from django.shortcuts import redirect
from django.urls import reverse_lazy



class AnonimousRequired:
    page_url = None
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.page_url)
        return super().dispatch(request, *args, **kwargs)


class UserRequired:
    page_url = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.page_url)
        return super().dispatch(request, *args, **kwargs)