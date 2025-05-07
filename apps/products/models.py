from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """Base model for every model"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']



class ProductConditionChoices(models.TextChoices):
    NEW = 'New', 'New'
    USED = 'Used', 'Used'
    REFURBISHED = 'Refurbished', 'Refurbished'



class ItemGroup(BaseModel):
    """Model to store the information of items groups"""
    name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name




class Brand(BaseModel):
    """Model to store the information of product's brand"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name




class GoogleProductCategory(BaseModel):
    """Model to store Google Product Category"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name




class ProductType(BaseModel):
    """Model to store product type"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Material(BaseModel):
    """Model to store material of product"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class Pattern(BaseModel):
    """Model to store pattern of product"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Color(BaseModel):
    """Model to store color of product"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    """Model to store product information"""
    track = models.ForeignKey('logs.FileUploadTrack', on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    sku = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    image_link = models.URLField()
    description = models.TextField(blank=True, null=True)
    link = models.URLField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    item_group = models.ForeignKey(ItemGroup, on_delete=models.PROTECT)
    # stock_quantity = models.PositiveIntegerField(default=0)
    availability = models.BooleanField(default=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    gtin = models.CharField(max_length=25)
    gender = models.CharField(max_length=25, blank=True, null=True)
    google_product_category = models.ForeignKey(GoogleProductCategory, on_delete=models.PROTECT)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    pattern = models.ForeignKey(Pattern, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    product_length = models.FloatField(blank=True, null=True)
    product_width = models.FloatField(blank=True, null=True)
    product_height = models.FloatField(blank=True, null=True)
    product_weight = models.FloatField(blank=True, null=True)
    size = models.CharField(max_length=25, blank=True, null=True)
    lifestyle_image_link = models.URLField(blank=True, null=True)
    max_handeling_time = models.IntegerField(blank=True, null=True)
    is_bundle = models.BooleanField(default=False)
    model = models.CharField(max_length=25)
    condition = models.CharField(max_length=15, choices=ProductConditionChoices.choices, default=ProductConditionChoices.NEW)


    
    def __str__(self):
        return f"{self.title} ({self.sku})"




class ProductAdditionalImages(BaseModel):
    """Model to store additional images of product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_image_links')
    image = models.URLField()

    def __str__(self):
        return self.product



class ProductShipping(BaseModel):
    """Model to store the shipping information of product"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='shipping')
    country = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product} {self.country}"
