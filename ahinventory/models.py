from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.
class StorageLocation(models.Model):
    prefix = models.CharField(max_length=50)
    index = models.IntegerField()
    location = models.CharField(max_length=50,blank=True)
    
    def __str__(self):
        return self.prefix+str(self.index)

class Category(MPTTModel):
    name = models.CharField(max_length=50,unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    def __str__(self):
        return self.name
    class MPTTMeta:
        order_insertion_by = ['name']
        
        
#class ItemManager(models.Manager):
#    def search(self,query=None):
#        qs = self.get_queryset()
#        if query is not None:
#            lookup = (Q(name__incontains=query))
            #or_lookup = (Q(title__icontains=query) | 
            #             Q(description__icontains=query)|
            #             Q(slug__icontains=query)
            #            )
#            qs = qs.filter(lookup).distinct()
#        return qs

class Item(models.Model):
    namevalue = models.CharField(max_length=50,unique=True)
    category  = TreeForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    quantity  = models.IntegerField()
    storelocation = models.ForeignKey(StorageLocation,on_delete=models.CASCADE,null=True,blank=True)
    image = ThumbnailerImageField(upload_to ='ahi/item/',blank=True)
#   ditambah file gambar

#    objects = ItemManager
    
    def __str__(self):
        return self.namevalue
        
        
    
