from django.shortcuts import render
from django.http import Http404

from catalogue.models import Price

# Create your views here.
def index(request):
    prices = Price.objects.all()
    title = 'Liste des prix'
    
    return render(request, 'price/index.html', {
        'prices':prices,
        'title':title
    })

def show(request, price_id):
    try:
        price = Price.objects.get(id=price_id)
    except Price.DoesNotExist:
        raise Http404('Prix inexistant');
        
    title = 'Fiche d\'un prix'
    
    return render(request, 'price/show.html', {
        'price':price,
        'title':title 
    })

