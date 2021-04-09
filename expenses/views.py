from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse

import json
from datetime import date, datetime
import decimal
# Create your views here.

from taxonomy.models import Taxonomy
from expenses.models import Expense


# TODO: render is reloading the page and removing previous data, prevent loss of data

def new_expense(request):
    # 'search-product': ['Milk:418'], 'purchase-date': ['2021-02-13'], 'purchase-price': ['11']
    if request.method == 'POST':

        search_filter = request.POST.get('search-product', None)

        # TODO: this : based decision is bad. how can I return an id
        if ':' not in search_filter:
            error_message = "Invalid search : " + search_filter
            return render(request, 'expenses/new-expense.html', {'error_message': error_message})

        prod_desc, prod_id = search_filter.split(':')
        product = Taxonomy.objects.get(pk=prod_id)
        if product is None:
            error_message = "Invalid Product: " + prod_desc
            return render(request, 'expenses/new-expense.html', {'error_message': error_message})

        # we now have a valid product with its id
        # TODO: Purchase date cannot be in future
        purchase_date_str = request.POST.get('purchase-date', None)
        if purchase_date_str is None:
            error_message = "Invalid Product Purchase Date: " + purchase_date_str
            return render(request, 'expenses/new-expense.html', {'error_message': error_message})
        try:
            purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date()
        except ValueError:
            error_message = "Error handling Product Purchase Date: " + purchase_date_str
            return render(request, 'expenses/new-expense.html', {'error_message': error_message})

        purchase_price_str = request.POST.get('purchase-price', None)
        if purchase_price_str is None:
            error_message = "Invalid Product Purchase Price: " + purchase_price_str
            return render(request, 'expenses/new-expense.html', {'error_message': error_message})

        try:
            purchase_price = decimal.Decimal(purchase_price_str)
        except (ValueError, decimal.DecimalException, decimal.InvalidOperation):
            error_message = "Error handling Product Purchase Price: " + purchase_price_str
            return render(request, 'expenses/new-expense.html', {'error_message': error_message})

        try:
            new_expense_req = Expense(date_of_purchase=purchase_date, purchase_price=purchase_price, product_id=product)
            new_expense_req.save()
        except ValidationError:
            error_message = "Error validating the expense form"
            return render(request, 'expenses/new-expense.html', {'error_message': error_message})

        # do httpredirect when success
        # TODO:  pass args (new_expense_req, ) to reverse so that this can be displayed in the list
        return HttpResponseRedirect(reverse('expenses:recent_expenses', args=None))
    else:
        return render(request, 'expenses/new-expense.html')


def filter_products(request):
    if request.is_ajax() and request.method == 'GET':
        product_filter = request.GET.get("product_filter", None)
        # get only first 10 elements
        product_details = Taxonomy.objects.values_list('product_description', 'taxonomy_id'). \
                              filter(product_description__icontains=product_filter).order_by('product_description')[:10]

        details_as_dict = json.dumps(dict(list(product_details)))
        return JsonResponse(details_as_dict, status=200, safe=False)

    return JsonResponse({}, status=400)


def recent_expenses(request):
    list_of_expenses = list(Expense.objects.values_list('id', 'date_of_purchase', 'product_id__product_description',
                                                        'purchase_price'))
    dict_of_expenses = {val[0]: val for val in list_of_expenses}
    print(dict_of_expenses)
    expenses_json = json.dumps(dict_of_expenses, cls=DjangoJSONEncoder)

    context = {
        'expenses_json': expenses_json,
        'page_title': f'List of Recent Expenses'
    }

    return render(request, 'expenses/recent-expenses.html', context)
