from django.test import TestCase
from django.urls import reverse

from .models import Taxonomy


class TaxonomyViewTests(TestCase):

    def test_no_products(self):
        """
        If no products found with a given description, an appropriate error message is displayed
        """
        url = reverse('taxonomy:taxonomy_list_by_description', args=('mjhgh',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)