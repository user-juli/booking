from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.text  import slugify
from ckeditor.fields import RichTextField

class Customer(models.Model):
    id = models.AutoField(primary_key = True)
    type_id = models.CharField(max_length = 100)
    numb = models.BigIntegerField()
    name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 120)
    email = models.EmailField(max_length = 200)
    phone = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

class Roomtype(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 120)
    people = models.IntegerField()
    price = models.DecimalField(max_digits = 9, decimal_places = 2)

    def __str__(self):
        return self.name

class Room(models.Model):
    class Status(models.TextChoices):
        DESOCUPADA = 'D', _('Desocupada')
        OCUPADA = 'O', _('Ocupada')
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 120)
    roomtype = models.ForeignKey('Roomtype',on_delete=models.CASCADE,)
    status = models.CharField(max_length=1,choices=Status.choices,default=Status.DESOCUPADA,)
    description = RichTextField()
    image_header = models.ImageField(upload_to='rooms/', default = 'rooms/None/no-img.jpg')
    url = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        super(Room, self).save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            url = self.image_header.url
        except:
            url = ''
        return url

def upload_gallery_image(instance, filename):
    return f"rooms/{instance.room.name}/{filename}"

class ImagesRoom(models.Model):
    image = models.ImageField(upload_to=upload_gallery_image)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.image.url))
        else:
            return '(No image)'

class Reservation(models.Model):
    class State(models.TextChoices):
        ESPERA = 'E', _('Espera')
        TOMADA = 'T', _('Tomada')
        CANCELADA = 'C', _('Cancelada')
    id = models.AutoField(primary_key = True)
    checkin = models.DateField()
    checkout = models.DateField()
    state = models.CharField(max_length=1,choices=State.choices,default=State.ESPERA,)
    adults = models.IntegerField()
    children = models.IntegerField()
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE,)
    room = models.ForeignKey('Room',on_delete=models.CASCADE,)
