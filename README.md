# issuetracker2

## Miembros del grup
|Nom                          |Taiga user         |Github user        |
| -------------               | -------------     | -------------     |
| Javier Rodríguez Carrasco   |javierrodriguezupc |javierrodriguezupc |
| Pau Carbó Pascual           |paucp1             |paucp1             |
| Santiago Lara Celis         |santilara16        |santilara16        |
| Toni Bosch Castells         |Toni Bosch         |tboschcastells     |         

## Deployed
- https://issuetracker2-asw.herokuapp.com/

## Framework utilizado
- Django


## Como crear el Virutal Enviroment
Entra en la raíz del protyecto y ejecuta:
  ```
  python -m venv env
  ```

## Como activar el Virutal Enviroment
  Entra en la raíz del protyecto y ejecuta el script Activate:
- Si se utilitza PowerShell:
  ```
  .\env\Scripts\Activate.ps1
  ```
- Si se utilitza Linux o Mac:
  ```
  source env/bin/activate
  ```

## como instalar las librerias:
Para actualitzar todas las librerias de python, con el Virutal Enviroment activado ejecuta (se requiere python>=3.8):
```
python -m pip install -r requirements.txt
```

## como hacer las migraciones:
Para hacer las migraciones, con el Virutal Enviroment activado ejecuta:
```
python manage.py makemigrations
```
```
python manage.py migrate
```

## como correr el servidor:
Para correr el server, con el Virutal Enviroment activado ejecuta:
```
python manage.py runserver
```

## Como instalar nuevas librerias:
Per instalar una llibreria python instalarla utilitzant pip:
```
python -m pip install LIBRARY_NAME
```
A continuació actualitzar el fitxer requirements.txt
```
python -m pip freeze > requirements.txt
```

# Como entrar a la rama develop
Primero comprobar en que rama estmos:
```
git status 
```
Nos lo indicarà diciendo: On branch <branch_name>

Ejecutar el comando:
```
git checkout develop 
```
Tras ejectuarlo deberia cambiar a la rama develop, para asegurarse volver a ejecutar git status y 
asegurarnos de que la rama actual es develop.

# Como crear una nueva rama
Crear una rama local:
```
git checkout -b <branch_name>
```
# Como convertir la rama local a remota
```
git push develop <local_branch>
```
