from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import requests
from .models import Issue
from .models import AttachedFile
import json

# Create your views here.import requests

@login_required(login_url='login')
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

@login_required(login_url='login')
@csrf_exempt
def new_issue_view(request):
    if request.method == 'POST':
        subject = request.POST.get('Subject')
        description = request.POST.get('Description')
        issue = {'Subject': subject,
                 'Description': description}
        print(issue)
        requests.post('http://127.0.0.1:8000/api/issues', json = issue)
        return redirect('allIssues')
        
    return render(request, 'new_issue.html')

@login_required(login_url='login')
@csrf_exempt
def delete_by_id(request):
    id = request.POST.get('id')
    Issue.objects.filter(id=id).delete()

    return issues_view(request)

@login_required(login_url='login')
def view_isue(request, issue_id):
    #Crida a la api per a obtenir tots els comments del issue
    comments = requests.get('http://127.0.0.1:8000/api/comments?id=' + str(issue_id))
    comments_json = comments.json()
    files = requests.get('http://127.0.0.1:8000/api/files?id=' + str(issue_id))
    files_json = files.json()
    issue = get_object_or_404(Issue, id=issue_id)
    issue = {'Subject': issue.Subject,
            'Description': issue.Description,
            'id': issue.id, 
            'status': issue.Status,
            'type': issue.Type,
            'severity': issue.Severity,
            'priority': issue.Priority,
            'DeadLine': issue.DeadLine}
    context = {'issue': issue,
               'comments': comments_json,
               'files': files_json}
    return render(request, 'issue_view.html', context)

@login_required(login_url='login')
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
    DeadLine = request.POST.get('DeadLine')

    if(issue.Subject != subject):
        issue.Subject = subject

    if(issue.Description != descripition):
        issue.Description = descripition

    if(issue.Status != status):
        issue.Status = status

    if(issue.Type != type):
        issue.Type = type

    if(issue.Severity != severity):
        issue.Severity = severity

    if(issue.Priority != priority):
        issue.Priority = priority

    if(issue.DeadLine != DeadLine):
        if(DeadLine == ''):
            issue.DeadLine = None
        else :            
            issue.DeadLine = DeadLine

    print('Aqui empieza el issue')
    print(issue.Subject)
    print(issue.Description)
    print(issue.Status)
    print(issue.Type)
    print(issue.Severity)
    print(issue.Priority)

    issue.save()

    return HttpResponseRedirect('/')

@login_required(login_url='login')
@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('Comment')
        issue = request.POST.get('id')
        comment_obj = {'Comment': comment,
                   'Issue': issue}
        print(comment_obj)
        requests.post('http://127.0.0.1:8000/api/comments', json = comment_obj)
        return HttpResponseRedirect('/issue/' + issue)
  


@login_required(login_url='login')
@csrf_exempt
def bulk_insert(request):
    if request.method == 'POST':
        issues = request.POST.get('issues')
        for line in issues.splitlines():
            print(line)
            issue = {'Subject': line}
            requests.post('http://127.0.0.1:8000/api/issues', json = issue)

    return render(request, 'bulk_insert.html')


@login_required(login_url='login')
@csrf_exempt
def add_file(request):
    if request.method == 'POST':
        issue = request.POST.get('id')
        file_obj = {'Issue': issue}
        print(file_obj)
        requests.post('http://127.0.0.1:8000/api/files', json = file_obj)
        return HttpResponseRedirect('/issue/' + issue)

@login_required(login_url='login')
@csrf_exempt
def delete_file(request):
    id = request.POST.get('id')
    issue = request.POST.get('issue')
    AttachedFile.objects.filter(id=id).delete()

    return view_isue(request, issue)