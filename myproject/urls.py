from django.contrib import admin
from django.urls import path
from myapp.views import login_view, image_upload_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'), 
    path('upload/', image_upload_view, name='upload'), 
]