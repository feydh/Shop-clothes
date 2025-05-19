from django.db import models
from django.shortcuts import render


class Category(models.Model):
     parent = models.ForeignKey('self', on_delete=models.CASCADE)
     name = models.CharField()

class Product(models.Model):
    def product_list(request):
        products = Product.objects.all()
        return render(request, 'admin_panel/product_list.html', {'products': products})

    image = models.ImageField(blank=True, upload_to='products/')
    name=models.CharField(  
        verbose_name=('Название товара'),
        max_length=50, 
    )  
  
    description=models.CharField(  
        verbose_name=('Опиание товара'),  
        max_length=100, 
    )  
  
    price=models.IntegerField(  
        verbose_name="Цена"  
    )  
    quantity=models.IntegerField(
        verbose_name=('Кол-во оставшихся')
    )
    categorys = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:  
        verbose_name="Товар"  
        verbose_name_plural="Товары"  
  
    def __str__(self):  
        return self.name