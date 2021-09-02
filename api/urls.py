from django.urls import path
# from .views import products
from .views import registration_view, OrderCreateView
      # ProductsDetailView, \
#     ProductsCreateView, BrandsCreateView, CountryCreateView, PhotoCreateView, CategoryCreateView, \
#     OrderCreateView, ProductsetCreateView, DiscountCreateView, Discount_pediodCreateView,\
#     Discount_brandCreateView
# from .views import brands, BrandsDetailView, country, CountryDetailView, photo, PhotoDetailView, \
#     category, CategoryDetailView, order, OrderDetailView, productset, ProductsetDetailView, discount, \
#     DiscountDetailView, discount_pediod, Discount_pediodDetailView, discount_brand, Discount_brandDetailView

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', registration_view.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('order/create/', OrderCreateView.as_view()),
    # path('products/<int:pk>/', ProductsDetailView.as_view()),
    # path('products/', products.as_view()),
    # path('products/create/', ProductsCreateView.as_view()),
    # path('brands/<int:pk>/', BrandsDetailView.as_view()),
    # path('brands/', brands.as_view()),
    # path('brands/create/', BrandsCreateView.as_view()),
    # path('country/<int:pk>/', CountryDetailView.as_view()),
    # path('country/', country.as_view()),
    # path('country/create/', CountryCreateView.as_view()),
    # path('photo/<int:pk>/', PhotoDetailView.as_view()),
    # path('photo/', photo.as_view()),
    # path('photo/create/', PhotoCreateView.as_view()),
    # path('category/<int:pk>/', CategoryDetailView.as_view()),
    # path('category/', category.as_view()),
    # path('category/create/', CategoryCreateView.as_view()),
    # path('order/<int:pk>/', OrderDetailView.as_view()),
    # path('order/', order.as_view()),
    # path('order/create/', OrderCreateView.as_view()),
    # path('productset/<int:pk>/', ProductsetDetailView.as_view()),
    # path('productset/', productset.as_view()),
    # path('productset/create/', ProductsetCreateView.as_view()),
    # path('discount/<int:pk>/', DiscountDetailView.as_view()),
    # path('discount/', discount.as_view()),
    # path('discount/create/', DiscountCreateView.as_view()),
    # path('discount_pediod/<int:pk>/', Discount_pediodDetailView.as_view()),
    # path('discount_pediod/', discount_pediod.as_view()),
    # path('discount_pediod/create/', Discount_pediodCreateView.as_view()),
    # path('discount_brand/<int:pk>/', Discount_brandDetailView.as_view()),
    # path('discount_brand/', discount_brand.as_view()),
    # path('discount_brand/create/', Discount_brandCreateView.as_view()),
]
