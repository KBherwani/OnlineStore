from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DeleteView, \
    UpdateView
import datetime
from django.contrib import auth, messages
from django.db.models import Q
from account.views import LoginRequired
from product.forms import ProductsForm, ImageFormset
from product.models import Product, ProductGallery


class ProductForm(LoginRequired, CreateView):
    template_name = "product_form.html"
    form_class = ProductsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset = ImageFormset(self.request.GET or None)
        context['form'] = self.form_class
        context['formset'] = formset
        return context

    def form_invalid(self, form):
        formset = ImageFormset(self.request.POST, self.request.FILES)
        form = self.form_class(self.request.POST, self.request.FILES)
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        formset = ImageFormset(self.request.POST, self.request.FILES)
        if form.is_valid() and formset.is_valid():
            form = form.save(commit=False)
            form.owner = self.request.user
            form.save()
            for formset_data in formset:
                obj = formset_data.save(commit=False)
                obj.product_id = form.pk
                obj.save()

        return redirect("product:product_list")


class ProductList(TemplateView):
    template_name = "product_list.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data()
        context['products'] = Product.objects.order_by('-id')
        return context


def search(request):
    search_keyword = request.GET.get('search')
    product = Product.objects.filter(Q(name__icontains=search_keyword)|Q(category__name__icontains=search_keyword))
    context = {'products': product,'search_keyword':search_keyword}
    template_name = "product_list.html"
    return render(request, template_name, context)


# class ProductDelete(DeleteView):
#     model = Product
#     success_url = reverse_lazy('product:product_list')
#     template_name = 'product_confirm_delete.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         class_obj = get_object_or_404(Product, id=kwargs.get('pk'))
#         if not self.request.user == class_obj.owner:
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form, *args, **kwargs):
#         self.object.delete()
#         return HttpResponseRedirect(self.success_url)


class UpdateProduct(LoginRequired, UpdateView):
    form_class = ProductsForm
    model = Product
    template_name = "update_product.html"
    success_url = reverse_lazy("product:product_list")

    def dispatch(self, request, *args, **kwargs, ):
        class_obj = get_object_or_404(Product, id=kwargs.get('pk'))
        if not self.request.user == class_obj.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        class_obj = get_object_or_404(Product, id=kwargs.get('pk'))
        form = ProductsForm(instance=class_obj)
        context = {}
        context["form"] = form
        context["data"] = class_obj
        'product:product_list'
        return render(request, self.template_name, context)

    def form_valid(self, form, *args, **kwargs):
        obj = form.save(commit=False)
        price = Product.objects.get(id=obj.pk).price
        if 'price' in form.changed_data:
            increase_price = price + (price * 0.1)
            decrease_price = price - (price * 0.1)
            if obj.price > increase_price or obj.price < decrease_price:
                messages.error(self.request,
                               "Product price can be updated with in Range of 10%")
                return super(UpdateProduct, self).form_invalid(form)
            if obj.price_updated:
                if not (datetime.datetime.utcnow() - obj.price_updated.replace(
                        tzinfo=None)) > datetime.timedelta(1):
                    messages.error(self.request,
                                   "Product price can be update only once a day")
                    return super(UpdateProduct, self).form_invalid(form)
                else:
                    obj.price_updated = datetime.datetime.now()
                    obj.save()
                    return super(UpdateProduct, self).form_valid(form)
            else:
                obj.price_updated = datetime.datetime.now()
                obj.save()

        form.save()
        return super(UpdateProduct, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        return super(UpdateProduct, self).form_invalid(form)


def view_product(request):
    if request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == "POST":
        product = Product.objects.get(pk=request.POST.get('pk'))
        # image2 = ProductGallery.objects.get(product=product.pk)
        image = ProductGallery.objects.filter(product=product.pk)
        context = {'obj': product, 'images': image}
        response = render_to_string('product_view.html', context)
        return JsonResponse({'status': 'success', 'html': response})


def delete_view(request):
    if request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == "POST":
        Product.objects.get(id=int(request.POST.get('pk'))).delete()
        msg = "Product Deleted Successfully"
        total_product = Product.objects.filter(owner=request.user).count()
        return JsonResponse({'status': 'success', 'message': msg,
                             'products': total_product, 'type': 'product',
                             'id': int(request.POST.get('pk'))})
