from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Create your models here.


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    starts_from=models.IntegerField(null=True)
    category_image= models.ImageField(upload_to="categories")
    is_listed=models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.category_name
    
class Sub_category(BaseModel):
    sub_category_name=models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.sub_category_name)
        super(Sub_category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.sub_category_name

class Attributes(BaseModel):
    name=models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Attribute_values(BaseModel):
    attribute=models.ForeignKey(Attributes, on_delete=models.CASCADE, related_name='attribute_values')
    value=models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.value


class Product(BaseModel):
    product_name=models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    Category = models.ForeignKey(Category, on_delete =models.CASCADE, related_name = "products")
    is_listed=models.BooleanField(default=False)
    is_category_listed=models.BooleanField(default=True)
    Sub_category=models.ForeignKey(Sub_category, on_delete=models.CASCADE,null=True, related_name='sub_category')
    price = models.IntegerField()
    product_description = models.TextField()
    # stock=models.IntegerField()


    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name

class ProductAttribute(BaseModel):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attributes')
    value=models.ManyToManyField(Attribute_values, related_name='product_attributes')
    new_price=models.IntegerField(null=True)        

    def __str__(self) -> str:
        values_str = ', '.join(str(value) for value in self.value.all())
        return f"{self.product.product_name} {values_str}"

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image= models.ImageField(upload_to="product")

    def __str__(self) -> str:
        return self.image.name
        
