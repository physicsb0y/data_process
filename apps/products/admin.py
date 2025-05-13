from django.contrib import admin
from .models import *

# Register your models here.

models = [
    ItemGroup, Brand, GoogleProductCategory, ProductType,
    Material, Pattern, Color, Product, ProductAdditionalImages,
    ProductShipping
]

for model in models:
    admin.site.register(model)
