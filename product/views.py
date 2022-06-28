from django.core.checks import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView, CreateView, DeleteView, \
    UpdateView

from account.views import LoginRequired
from product.forms import ProductsForm
from product.models import Product


class ProductForm(LoginRequired, CreateView):
    template_name = "product_form.html"
    form_class = ProductsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def form_invalid(self, form):
        form = self.form_class(self.request.POST)
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        form = form.save(commit=False)
        form.owner = self.request.user
        form.save()
        return redirect("product:product_list")


class ProductList(TemplateView):
    template_name = "product_list.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data()
        context['products'] = Product.objects.all()
        template = self.template_name
        return context


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product:product_list')
    template_name = 'product_confirm_delete.html'

    def form_valid(self, form):
        self.object.delete()
        return HttpResponseRedirect(self.success_url)


class UpdateProduct(LoginRequired, UpdateView):
    form_class = ProductsForm
    model = Product
    template_name = "update_product.html"
    success_url = reverse_lazy  ("product:product_list")

    def dispatch(self, request, *args, **kwargs):
        class_obj = get_object_or_404(Product, id=kwargs.get('pk'))
        if not self.request.user == class_obj.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,  *args, **kwargs):
        class_obj = get_object_or_404(Product, id=kwargs.get('pk'))
        form = ProductsForm(instance=class_obj)
        context = {}
        context["form"] = form
        context["data"] = class_obj
        'product:product_list'
        return render(request, self.template_name, context)

    def form_valid(self, form, *args, **kwargs):
        form.save()
        return super(UpdateProduct, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        return redirect("product:product_list")
