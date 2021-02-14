from django.db import models
from datetime import datetime

from taxonomy.models import Taxonomy


# Make a model for expense which is represented by default id, product id (what you bought),
# date (mm-dd-yyyy) and the price ( 2 decimals)


class Expense(models.Model):
    date_of_purchase = models.DateField(default=datetime.today, null=False)
    product_id = models.ForeignKey(Taxonomy, on_delete=models.PROTECT, null=False)
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)

    def __str__(self):
        return f'<Product: {self.product_id.product_description}, Date of Purchase: {self.date_of_purchase}, ' \
               f'Purchase Price: {self.purchase_price}'
