from django.urls import path
from .views import registration_view, OrderCreateView, order
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('register/', registration_view.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('order/create/', OrderCreateView.as_view(), name='order-create'),
    path('order/', order.as_view(), name='order'),
]
