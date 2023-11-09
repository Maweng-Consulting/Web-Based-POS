from table import Table
from table.columns import Column

from inventory.models import Inventory


class InventoryTable(Table):
    id = Column(field='id')
    name = Column(field='name')
    buying_price = Column(field='buying_price')
    selling_price = Column(field='selling_price')
    quantity = Column(field='quantity')
    class Meta:
        model = Inventory
