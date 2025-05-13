import decimal
import re
import logging
from decimal import Decimal, InvalidOperation
from django.db import transaction
from .models import *
from apps.products.models import *


REQUIRED_FIELDS = ['id', 'title', 'price', 'brand', 'item_group_id']

def parce_decimal(price_str):
    match = re.search(r'\d+(?:[.,]\d+)?', price_str)
    if match:
        try:
            num_str = match.group().replace(',', '.')
            return Decimal(num_str)
        except (InvalidOperation, ValueError, decimal.ConversionSyntax) as e:
            return None
    return None



def validate_row(data):
    errors = []
    warnings = []

    for field in REQUIRED_FIELDS:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")

    if not data.get('description'):
        warnings.append("Missing description")

    price_str = str(data.get('price', '')).strip()
    logging.info("PRICE: %s", price_str)

    price_decimal = parce_decimal(price_str)
    if price_decimal is None:
        errors.append("Invalid price format")
    else:
        print("PRICE DECIMAL: ", price_decimal)
  

    return errors, warnings

def get_or_create_related_model(model, name):
    if not name or not isinstance(name, str):
        return None
    instance, _ = model.objects.get_or_create(name=name.strip())
    return instance

def parse_shipping_field(shipping_str):
    if not shipping_str:
        return []

    entries = shipping_str.split(',')
    shipping_data = []

    for entry in entries:
        try:
            country, price_str = entry.split(':')
            price_str = price_str.strip()


            numeric_match = re.search(r'[\d\.,]+', price_str)
            if not numeric_match:
                raise ValueError(f"No numeric value found in '{price_str}'")
            price = Decimal(numeric_match.group().replace(',', '.'))


            currency_match = re.search(r'[A-Z]{3}$', price_str)
            currency = currency_match.group() if currency_match else 'UNKNOWN'

            shipping_data.append({
                'country': country.strip(),
                'price': price,
                'currency': currency
            })

        except (ValueError, InvalidOperation) as e:
            print(f"Error parsing shipping field: {e}")
            continue

    return shipping_data
def create_product_from_row(data, file_track):
    logging.info("Creating product from row: %s, %s", data, data.get('google_product_category'))
    with transaction.atomic():
        logging.info("Product category id: %s", data.get('google_product_category'))
        brand = get_or_create_related_model(Brand, data.get('brand'))
        item_group = get_or_create_related_model(ItemGroup, data.get('item_group_id'))
        gpc = get_or_create_related_model(GoogleProductCategory, str(data.get('google_product_category')))
        ptype = get_or_create_related_model(ProductType, data.get('product_type'))
        material = get_or_create_related_model(Material, data.get('material'))
        pattern = get_or_create_related_model(Pattern, data.get('pattern'))
        color = get_or_create_related_model(Color, data.get('color'))
        logging.info("Saving: %s, %s, %s, %s, %s, %s, %s, %s", data.get('id'), brand, item_group, gpc, ptype, material, pattern, color)
        product = Product.objects.create(
            track=file_track,
            sku=data['id'],
            title=data['title'],
            image_link=data.get('image_link'),
            description=data.get('description'),
            link=data.get('link'),
            price=parce_decimal(data['price']),
            sale_price=parce_decimal(data['sale_price']) if data.get('sale_price') else None,
            item_group=item_group,
            availability=str(data.get('availability')).lower() in ['1', 'true', 'yes'],
            brand=brand,
            gtin=data.get('gtin', ''),
            gender=data.get('gender'),
            google_product_category=gpc,
            product_type=ptype,
            material=material,
            pattern=pattern,
            color=color,
            product_length=data.get('product_length') or 0,
            product_width= data.get('product_width') or 0,
            product_height=data.get('product_height') or 0,
            product_weight=data.get('product_weight') or 0,
            size=data.get('size'),
            lifestyle_image_link=data.get('lifestyle_image_link'),
            max_handeling_time=int(data.get('max_handling_time') or 0),
            is_bundle=str(data.get('is_bundle')).lower() in ['1', 'true', 'yes'],
            model=data.get('Model', '')[:25],
            condition=data.get('condition', ProductConditionChoices.NEW),
        )

        for url in str(data.get('additional_image_links', '')).split(','):
            if url.strip():
                ProductAdditionalImages.objects.create(product=product, image=url.strip())

        for shipping_entry in parse_shipping_field(data.get('shipping(country:price)')):
            ProductShipping.objects.create(product=product, **shipping_entry)

        return product
    return None
