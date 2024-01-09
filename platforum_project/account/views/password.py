from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy


class UserChangePassword(PasswordChangeView):
    template_name = "password/change-form.html"
    success_url = reverse_lazy("account:password-done")


class UserPasswordDone(PasswordChangeDoneView):
    template_name = "password/change-done.html"


class UserResetPassword(PasswordResetView):
    template_name = "password/reset.html"
    success_url = reverse_lazy("account:reset-done")
    email_template_name = "password/reset-email.html"


class UserResetDone(PasswordResetDoneView):
    template_name = "password/reset-done.html"


class UserResetConfirm(PasswordResetConfirmView):
    template_name = "password/reset-confirm.html"
    success_url = reverse_lazy("account:reset-complete")


class UserResetComplete(PasswordResetCompleteView):
    template_name = "password/reset-complete.html"
