from apps.inventory.models import Inventory, InventoryLog


class UploadNewStockMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__upload_new_stock()

    def __upload_new_stock(self):
        items = self.data

        items_list = []

        for item in items:
            print(item)

            items_list.append(
                Inventory(
                    name=item["name"].strip(),
                    buying_price=item["buying_price"].strip(),
                    selling_price=item["selling_price"].strip(),
                    quantity=item["quantity"].strip(),
                    category_id=item["category"].strip(),
                    unit_of_measure=item["unit_of_measure"].strip(),
                )
            )

        Inventory.objects.bulk_create(items_list)
        print("*******Products Created Successfully!!************")
