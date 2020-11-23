from django.shortcuts import render

# Create your views here.
def standings_page(request):
    return render(request, 'standings/standings.html')