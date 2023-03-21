import requests
from ..issues import models
from django.shortcuts import render

def lista_issues(request):
    response = requests.get('http://127.0.0.1:8000/api/issues')
    issues = response.json()
    return render(request, 'issues.html', {'issues': issues})
