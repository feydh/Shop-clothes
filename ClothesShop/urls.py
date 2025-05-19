from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v0/user/', include('users.urls')),
    # path('api/v0/products/', include('products.urls')),
    # path('', include('website.urls')),
]
