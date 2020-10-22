from django.shortcuts import render
import pandas as pd
from rushers import forms
# Create your views here.

def rusher_page(request):
    print('in rushers page!!!!')
    return render(request, 'rushers/rusher.html')