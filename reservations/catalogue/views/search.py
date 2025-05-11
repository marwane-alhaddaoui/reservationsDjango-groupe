from django.shortcuts import render
from catalogue.models import Show, Representation
from django.db.models import Q

def search(request):
    q = request.GET.get('q', '').strip()
    shows = []
    reps = []
    if q:
        shows = Show.objects.filter(title__icontains=q)
        reps  = Representation.objects.filter(
            Q(show__title__icontains=q) |
            Q(location__designation__icontains=q)
        )
    return render(request, 'search.html', {
        'query': q,
        'shows': shows,
        'representations': reps,
    })
