import csv


def trim_product_line(pl):
    ind = len(pl)
    for ind in range(len(pl) - 1, 0, -1):
        if pl[ind] != '':
            break

    return pl[:ind + 1]


"""
The product taxonomy from Google is organized in as 
(product identifier, parent description, optional one or more parent description, product description)
This can be modeled as <product identifier, parent product identifier, product description>
For products that do not have a parent, parent product identifier will be same as product identifier

Some of the text contains a ' like "Chef's Hats" . This is addressed by quotechar="'"  
"""


def read_product_taxonomy_data(taxonomy_data):
    taxonomy_dict = {}
    temp_lookup_pid = {}
    with open(taxonomy_data) as product_fp:
        product_reader = csv.reader(product_fp, quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for product_line in product_reader:
            # go from right to left in the product_line list and weed out empty entries
            product_line = trim_product_line(product_line)
            # first entry is always product id
            pid = str(product_line[0])
            product_description = product_line[-1]
            temp_lookup_pid[product_description] = pid
            # here is the logic for identifying the parent id
            # if the product line indeed has a parent, it will have at least 3 entries,
            # the second last of which will be the immediate parent of the product
            # otherwise we just use the product id itself as parent id
            if len(product_line) > 2:
                product_parent_id = temp_lookup_pid[product_line[-2]]
            else:
                product_parent_id = None

            taxonomy_dict[pid] = (product_parent_id, product_description)

    return taxonomy_dict

