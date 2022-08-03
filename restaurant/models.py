from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from phonenumber_field.modelfields import PhoneNumberField


class SingletonBaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).get_queryset().filter(available=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("restaurant:home_by_category", args=[self.slug])
    

 
class Food(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    image = models.ImageField(upload_to="foods/%Y/%m/%d")
    description = HTMLField(blank=True)
    category = models.ForeignKey(Category, related_name='foods', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    objects_available = AvailableManager()
    
    class Meta:
        ordering = ('-created', )
        index_together = (('id', 'slug'), ) 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant:food_detail', kwargs={'slug': self.slug})
        
    
class Employee(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='first name')
    last_name = models.CharField(max_length=100, verbose_name='last name')
    image = models.ImageField()
    position = models.CharField(max_length=100)
    description = models.TextField()
    instagram = models.URLField(null=True, blank=True)
    tweeter = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name 
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name 
    


class About(SingletonBaseModel):
    description = HTMLField()
    
    def __str__(self) -> str:
        return self.description


class History(SingletonBaseModel):
    description = HTMLField()   

    def __str__(self) -> str:
        return self.description


class Address(SingletonBaseModel):
    description = models.TextField(max_length=200, verbose_name='full address')
    phone_number = PhoneNumberField()
    email = models.EmailField()
    tweeter = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)


    def __str__(self) -> str:
        return self.description


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self) -> str:
        return self.name 



