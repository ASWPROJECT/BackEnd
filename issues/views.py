from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import requests
from .models import Issue

# Create your views here.import requests

def issues_view(request):
    # Hacer la solicitud GET a la API

    response = requests.get('http://127.0.0.1:8000/api/issues')
    
    # Obtener los datos de la respuesta de la API
    data = response.json()
    context = {'issues': data}
    
    # Renderizar la plantilla HTML y pasar los datos de los resultados
    return render(request, 'issues.html', context)

@csrf_exempt
def new_issue_view(request):
    if request.method == 'POST':
        subject = request.POST.get('Subject')
        description = request.POST.get('Description')
        issue = {'Subject': subject,
                 'Description': description}
        print(issue)
        requests.post('http://127.0.0.1:8000/api/issues/', json = issue)
        
    return render(request, 'new_issue.html')

@csrf_exempt
def delete_by_id(request):
    id = request.POST.get('id')
    Issue.objects.filter(id=id).delete()

    return issues_view(request)