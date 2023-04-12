from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import AsignedUser, Issue, Activity, Watcher
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import json

# Create your views here.import requests

def issues_view(request):
    params = request.GET
    q = params.get('q', '')
    # Hacer la solicitud GET a la API
    response = requests.get('http://127.0.0.1:8000/api/issues?q=' + q)
    
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
        requests.post('http://127.0.0.1:8000/api/issues', json = issue)
        
    return render(request, 'new_issue.html')

@csrf_exempt
def delete_by_id(request):
    id = request.POST.get('id')
    Issue.objects.filter(id=id).delete()

    return issues_view(request)


def view_isue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    User = get_user_model()
    users = User.objects.all()
    activities = None
    try:
        activities = Activity.objects.filter(issue = issue)
    except Http404:
        print('No tiene activities')

    issue = {'Subject': issue.Subject,
            'Description': issue.Description,
            'id': issue.id, 
            'status': issue.Status,
            'type': issue.Type,
            'severity': issue.Severity,
            'priority': issue.Priority,
            'users': users,
            'activities': activities}
    context = {'issue': issue}
    return render(request, 'issue_view.html', context)

@csrf_exempt
def edit_issue(request):
    id = request.POST.get('id')
    issue = get_object_or_404(Issue, id=id)

    subject = request.POST.get('Subject')
    descripition = request.POST.get('Description')
    status = request.POST.get('status')
    type = request.POST.get('type')
    severity = request.POST.get('severity')
    priority = request.POST.get('priority')
    watchers = request.POST.getlist('watchers[]')
    users_asigned = request.POST.getlist('asigned_users[]')
    print('-------------')
    print(priority)
    print(severity)
    print(type)
    print('-------------')


    if(len(watchers) > 0):
        for watcher in watchers:
            Watcher.objects.create(
            User = User.objects.get(username=watcher),
            Issue = issue,
            )


    if(len(users_asigned) > 0):
        for user in users_asigned:
            AsignedUser.objects.create(
            User = User.objects.get(username=user),
            Issue = issue,
            )
            Activity.objects.create(
                creator = User.objects.get(username='santi'),
                issue = issue,
                type = "assigned to",
                user = User.objects.get(username=user)
            )    

    if(issue.Subject != subject or subject != ''):
        issue.Subject = subject

    if(issue.Description != descripition and descripition != 'None'):
        issue.Description = descripition
        
        Activity.objects.create(
                creator = User.objects.get(username='santi'),
                issue = issue,
                type = "description"
        )

    if(issue.Status != status):
        issue.Status = status

    if(issue.Type != type and type != ""):
        issue.Type = type
        
        Activity.objects.create(
                creator = User.objects.get(username='santi'),
                issue = issue,
                type = "type"
        )

    if(issue.Severity != severity and severity != ""):
        issue.Severity = severity
        
        Activity.objects.create(
                creator = User.objects.get(username='santi'),
                issue = issue,
                type = "severity"
        )

    if(issue.Priority != priority and priority != ""):
        issue.Priority = priority

        Activity.objects.create(
                creator = User.objects.get(username='santi'),
                issue = issue,
                type = "priority"
        )

    issue.save()

    return HttpResponseRedirect('/')


@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('Comment')
        issue = request.POST.get('Issue')
        comment_obj = {'Comment': comment,
                   'Issue': issue}
        print(comment_obj)
        requests.post('http://127.0.0.1:8000/api/comments', json = comment_obj)
    
    #Crida a la api per a obtenir tots els comments
    response = requests.get('http://127.0.0.1:8000/api/comments')
    data = response.json()
    context = {'comments': data}
    return render(request, 'comments.html', context)


@csrf_exempt
def bulk_insert(request):
    if request.method == 'POST':
        issues = request.POST.get('issues')
        for line in issues.splitlines():
            print(line)
            issue = {'Subject': line}
            requests.post('http://127.0.0.1:8000/api/issues', json = issue)

    return render(request, 'bulk_insert.html')


def remove_all_activities(request):
    Watcher.objects.all().delete()