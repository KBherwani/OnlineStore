from django.urls import path

from .views import *

app_name = "product"

urlpatterns = [
    path("form/", ProductForm.as_view(), name="product_form"),
    path("list/", ProductList.as_view(), name="product_list"),
    path("update/<int:pk>/", UpdateProduct.as_view(), name="update_product"),
    # path("delete/<int:pk>/", ProductDelete.as_view(), name="delete_product"),
    path("search/", search, name="search"),
    path("view-product/", view_product, name="view_product"),
    path("delete-product/", delete_view, name="delete_view"),


]
