from django.contrib import admin
from . models import Customer,Roomtype,Room,Reservation,ImagesRoom

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'numb', 'name', 'last_name')

@admin.register(Roomtype)
class RoomtypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'people', 'price')

class ImageInline(admin.TabularInline):
    model = ImagesRoom
    readonly_fields = ('image_preview',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'roomtype', 'image_header', 'status')
    inlines = [
        ImageInline
    ]

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('url', )
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        return form

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'checkin', 'checkout', 'state', 'customer')
