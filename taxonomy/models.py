import pkgutil

from django.conf import settings
from django.db import models

import data
from data import product_taxonomy


# Create your models here.


class Taxonomy(models.Model):
    taxonomy_id = models.CharField(primary_key=True, max_length=10)
    # self referencing foreign key
    parent_id = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    product_description = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"<Product ID: {self.taxonomy_id} , Parent Id: {self.parent_id}, Product Description: {self.product_description}>"

    @classmethod
    def load_taxonomy_to_model(cls):
        taxonomy_data = settings.DATA_PATH + "product_taxonomy_google.csv"
        taxonomy_dict = product_taxonomy.read_product_taxonomy_data(taxonomy_data)

        for key, val in taxonomy_dict.items():
            print(key)
            print(val[0])
            print(val[1])
            parent_instance = None
            if val[0] is not None:
                parent_instance = Taxonomy.objects.get(pk=val[0])
            print(parent_instance)
            t = Taxonomy(taxonomy_id=key, parent_id=parent_instance, product_description=val[1])
            # t = Taxonomy("3237", "1", "Live Animals")
            t.save()
            print(t)

