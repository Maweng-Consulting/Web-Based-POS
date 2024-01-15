import json

from .models import Inventory
from .sample_products import sample_products


def load_sample_products():
    products_list = []

    for item in sample_products:
        products_list.append(
            Inventory(
                name=item["name"],
                buying_price=item["buying_price"],
                selling_price=item["selling_price"],
                quantity=item["quantity"],
                unit_of_measure=item["unit_of_measure"],
            )
        )

    Inventory.objects.bulk_create(products_list)
    print(
        "************************Products Created Successfully!!************************"
    )
