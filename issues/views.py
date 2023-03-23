from django.shortcuts import render
import requests

# Create your views here.import requests

def issues_view(request):
    # Hacer la solicitud GET a la API
    response = requests.get('http://127.0.0.1:8000/api/issues')
    
    # Obtener los datos de la respuesta de la API
    data = response.json()
    context = {'issues': data}
    
    # Renderizar la plantilla HTML y pasar los datos de los resultados
    return render(request, 'templates/issues.html', context)

