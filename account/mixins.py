from django.http import Http404
from django.shortcuts import redirect

       
class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("You can't see this page!!!")
        else:
            return redirect('login')
       