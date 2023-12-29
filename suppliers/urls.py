from django.urls import path

from suppliers.views import (delete_supplier, edit_supplier, new_supplier,
                             supplier_details, suppliers)

urlpatterns = [
    path("", suppliers, name="suppliers"),
    path("<int:supplier_id>/", supplier_details, name="supplier-details"),
    path("new-supplier/", new_supplier, name="new-supplier"),
    path("edit-supplier/", edit_supplier, name="edit-supplier"),
    path("delete-supplier/", delete_supplier, name="delete-supplier"),
]