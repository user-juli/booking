from django.shortcuts import render
from .models import Room,Roomtype,Reservation,ImagesRoom
from django.views.generic import TemplateView,DetailView,ListView,CreateView
from .forms import BookingForm

class HomeView(TemplateView):
    template_name = 'index.html'

class SearchView(ListView):
    template_name = 'search.html'
    model = Room
    context_object_name = 'search'
    paginate_by = 15

    def get_queryset(self):
        adults = int(self.request.GET.get('a'))
        children = int(self.request.GET.get('c'))
        query = adults + children
        results = Room.objects.all().values('name','description','status','image_header','url','roomtype__name','roomtype__price','roomtype__people').filter(status='D',roomtype__people=query)
        return results
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['srooms']= self.get_queryset()
        return context


class BedroomDetailView(DetailView):
    template_name = 'available.html'
    model = Room
    context_object_name = 'available'
    slug_field = 'url'
    slug_url_kwarg = 'url'

    def get_queryset(self):
        return self.model.objects.filter(url=self.kwargs['url'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.all().values('id','name','description','status','image_header','url','roomtype__name','roomtype__price','roomtype__people').filter(status='D')
        context['imagesroom'] = ImagesRoom.objects.filter(room=self.get_object()).all()
        return context


"""
class BookingView(CreateView):
    model: Reservation
    form_class: BookingForm
    template_name: 'booking.html'
    context_object_name: 'booking'

    def get_success_url(self):
        return reverse('available', args = [self.object.room.id])

    def form_valid(self, form):
        form.instance.room = Room.objects.get(id=self.kwargs.get('pk'))

        return super().form_valid(form)
"""
