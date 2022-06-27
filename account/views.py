from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, TemplateView, FormView
from .forms import SignUpForm, UserLoginForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.utils.encoding import force_str


class HomeView(TemplateView):
    """
    Used to render homepage
    """
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SignUpView(View):
    form_class = SignUpForm
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, (
                'Please Confirm your email to complete registration.'))

            return redirect("account:login")

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('account:home')
        else:
            messages.warning(request, (
                'The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('account:home')


class LoginView(FormView):
    """
        Used to manage User Login view
    """
    form_class = UserLoginForm
    template_name = "login.html"

    def form_valid(self, form):
        user = form.cleaned_data
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect("account:login")

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogoutView(FormView):
    """
        Used to manage User Logout View
    """

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, "User logged out successfully.")
        return redirect("account:login")
