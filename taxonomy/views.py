from django.shortcuts import render, get_object_or_404, get_list_or_404, Http404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json

from .models import Taxonomy


def list_all(request):
    list_of_taxonomies = Taxonomy.objects.values_list('taxonomy_id', 'product_description').order_by('taxonomy_id')

    tmp_json = json.dumps(dict(list(list_of_taxonomies)))
    context = {
        'dict_of_taxonomies': tmp_json,
        'page_tile': f'List of all Products'
    }
    return render(request, 'taxonomy/index.html', context)


def list_by_descr(request, product_description):
    product_details = Taxonomy.objects.values_list('taxonomy_id', 'product_description').\
            filter(product_description__icontains=product_description).order_by('product_description')
    if len(list(product_details)) == 0:
        raise Http404(f"No Product Taxonomies with this description {product_description}")

    tmp_json = json.dumps(dict(list(product_details)))
    return render(request, 'taxonomy/index.html', {'dict_of_taxonomies': tmp_json,
                                                   'page_title': f'List of all Products with description: {product_description}'})


def list_by_id(request, product_id):
    product_details = get_object_or_404(Taxonomy, pk=product_id)
    return render(request, 'taxonomy/product-details.html', {'product_details': product_details,
                                                             'page_title': f'Product Details for ID: {product_id}'})


def list_by_parent_id(request, product_id):
    product_details = Taxonomy.objects.values_list('taxonomy_id', 'product_description'). \
        filter(parent_id=product_id).order_by('taxonomy_id')

    if len(list(product_details)) == 0:
        raise Http404(f"No Product Taxonomies with this Parent ID: {product_id}")

    tmp_json = json.dumps(dict(list(product_details)))
    return render(request, 'taxonomy/index.html', {'dict_of_taxonomies': tmp_json,
                                                   'page_title': f'List of all Products with Parent ID: {product_id}'})