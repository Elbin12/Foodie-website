from django.db import models
from base.models import BaseModel

# Create your models here.




class Banner(BaseModel):
    image=models.ImageField(upload_to="banners")
    order=models.IntegerField(unique=True, null=True, blank=True)

class Pdf(models.Model):
    pdf=models.FileField(upload_to='pdf', blank=True)