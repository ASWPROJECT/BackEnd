from django.shortcuts import render
import requests

# Create your views here.import requests

def lista_issues(request):
    # Hacer la solicitud GET a la API
    response = requests.get('http://127.0.0.1:8000/api/issues')
    
    # Obtener los datos de la respuesta de la API
    resultados = response.json()
    print("hola")
    print(resultados)
    
    # Renderizar la plantilla HTML y pasar los datos de los resultados
    return render(request, 'frontend/issues.html', {'issues': resultados})

