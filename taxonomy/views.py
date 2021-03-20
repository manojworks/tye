from django.shortcuts import render, get_object_or_404, get_list_or_404, Http404
from django.views import generic
import json

from .models import Taxonomy


def list_all(request):
    list_of_taxonomies = Taxonomy.objects.values_list('taxonomy_id', 'product_description').order_by('taxonomy_id')

    tmp_json = json.dumps(dict(list(list_of_taxonomies)))
    context = {
        'dict_of_taxonomies': tmp_json,
        'page_title': f'List of all Products'
    }
    return render(request, 'taxonomy/index.html', context)


def list_by_descr(request, product_description):
    product_details = Taxonomy.objects.values_list('taxonomy_id', 'product_description').\
            filter(product_description__icontains=product_description).order_by('product_description')
    if len(list(product_details)) == 0:
        # TODO Instead of silly 404 show a better message on same page
        raise Http404(f"No Product Taxonomies with this description {product_description}")

    tmp_json = json.dumps(dict(list(product_details)))
    return render(request, 'taxonomy/index.html', {'dict_of_taxonomies': tmp_json,
                                                   'page_title': f'List of all Products with description: {product_description}'})


class ProductDetailsView(generic.DetailView):
    model = Taxonomy
    template_name = 'taxonomy/product-details.html'
    context_object_name = 'product_details'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailsView, self).get_context_data(**kwargs)
        context['page_title'] = f'Product Details for ID:' + self.kwargs['pk']
        return context


def list_by_parent_id(request, product_id):
    product_details = Taxonomy.objects.values_list('taxonomy_id', 'product_description'). \
        filter(parent_id=product_id).order_by('taxonomy_id')

    if len(list(product_details)) == 0:
        # TODO Show a better page when not found
        raise Http404(f"No Product Taxonomies with this Parent ID: {product_id}")

    tmp_json = json.dumps(dict(list(product_details)))
    return render(request, 'taxonomy/index.html', {'dict_of_taxonomies': tmp_json,
                                                   'page_title': f'List of all Products with Parent ID: {product_id}'})