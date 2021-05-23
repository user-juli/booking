from django.shortcuts import render
from .models import Room,Roomtype
from django.views.generic import TemplateView,DetailView,ListView

class HomeView(TemplateView):
    template_name = "index.html"

class SearchView(ListView):
    template_name = 'available.html'
    model = Room
    context_object_name = 'search'

    def get_queryset(self):
        adults = int(self.request.GET.get('a'))
        children = int(self.request.GET.get('c'))
        query = adults + children
        results = Room.objects.all().values('name','description','status','image_header','url','roomtype__name','roomtype__price','roomtype__people').filter(status='D',roomtype__people=query)
        return results


class BedroomDetailView(DetailView):
    template_name = 'booking.html'
    model = Room
    context_object_name = 'booking'
    slug_field = 'url'
    slug_url_kwarg = 'url'

    def get_queryset(self):
        return self.model.objects.filter(url=self.kwargs['url'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
