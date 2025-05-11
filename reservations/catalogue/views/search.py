from django.shortcuts import render
from catalogue.models import Show, Representation
from catalogue.models import Artist

from django.db.models import Q

def search(request):
    query = request.GET.get('q', '').strip()

    shows = Show.objects.filter(title__icontains=query)
    representations = Representation.objects.filter(
        show__title__icontains=query
    )

    artists = Artist.objects.filter(
        Q(firstname__icontains=query) |
        Q(lastname__icontains=query)
    )

    return render(request, 'search/results.html', {
        'query': query,
        'shows': shows,
        'representations': representations,
        'artists': artists,
    })
