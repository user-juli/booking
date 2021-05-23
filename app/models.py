from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text  import slugify

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
    description = models.TextField()
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

class Reservation(models.Model):
    class State(models.TextChoices):
        ESPERA = 'E', _('Espera')
        TOMADA = 'T', _('Tomada')
        CANCELADA = 'C', _('Cancelada')
    id = models.AutoField(primary_key = True)
    checkin = models.DateTimeField()
    checkout = models.DateTimeField()
    state = models.CharField(max_length=1,choices=State.choices,default=State.ESPERA,)
    adults = models.IntegerField()
    children = models.IntegerField()
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE,)
    room = models.ForeignKey('Room',on_delete=models.CASCADE,)
