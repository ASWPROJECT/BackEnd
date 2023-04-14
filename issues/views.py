from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import requests
from .models import AsignedUser, Issue, Activity, Watcher
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Issue
from .models import AttachedFile
import json

URI = 'https://issuetracker2.onrender.com/'

# Create your views here.import requests

@login_required(login_url='login')
def issues_view(request):
    params = request.GET
    url = URI+'api/issues?'
    q = params.get('q', '')
    if q != '':
        url = url + "q=" + q
    
    status = params.get('status', '')
    if status != '':
        url = url + "&status=" + status

    priority = params.get('priority', '')
    if priority != '':
        url = url + "&priority=" + priority
    
    creator = params.get('creator', '')
    if creator != '':
        url = url + "&creator=" + creator
    
    order_by = params.get('order_by', '')
    if order_by != '':
        url = url + "&order_by=" + order_by
    # Hacer la solicitud GET a la API
    print(url)
    response = requests.get(url)
    User = get_user_model()
    users = User.objects.all()
    
    # Obtener los datos de la respuesta de la API
    data = response.json()
    context = {'issues': data,
               'users': users}
    
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
        requests.post(URI+'api/issues', json = issue)
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
    comments = requests.get(URI+'api/comments?id=' + str(issue_id))
    comments_json = comments.json()
    files = requests.get(URI+'api/files?id=' + str(issue_id))
    files_json = files.json()
    issue = get_object_or_404(Issue, id=issue_id)
    User = get_user_model()
    users = User.objects.all()
    activities = None
    w_names = []
    try:
        for w in Watcher.objects.filter(Issue=issue):
            w_names.append(w.User.username)
    except:
        print('No hay watchers')


    a_names = []
    try:
        for ass in AsignedUser.objects.filter(Issue=issue):
            a_names.append(ass.User.username)
    except:
        print('No hay asignedUsers')

    
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
            'watchers': w_names,
            'asignedusers': a_names,
            'activities': activities,
            'DeadLine': issue.DeadLine,
            'Block_reason': issue.Block_reason}
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
    watchers = request.POST.getlist('watchers[]')
    users_asigned = request.POST.getlist('asigned_users[]')
    
    watchers_users_selected = []

    for w in watchers:
        watchers_users_selected.append(User.objects.get(username = w))
    
    watchers_db = []

    try:
        for user in watchers_users_selected:    
            watchers_db.append(Watcher.objects.filter(Issue = issue).exclude(User = user))
    except Http404:
        print('No tiene watchers en la base de datos')

    asigned_users_selected = []

    for u in users_asigned:
        asigned_users_selected.append(User.objects.get(username = u))
    
    asigned_users_db = []

    try:
        for user in asigned_users_selected:    
            asigned_users_db.append(AsignedUser.objects.filter(Issue = issue).exclude(User = user))
    except Http404:
        print('No tiene watchers en la base de datos')


    if(len(watchers) > 0):
        for w in watchers_db:
            w.delete()
        try:
            for w in watchers:
                Watcher.objects.create(
                    User = User.objects.get(username = w),
                    Issue = issue,
                )
        except:
            print("Ya existe")
    else:
        Watcher.objects.filter(Issue = issue).delete()


    if(len(users_asigned) > 0):
        for u in asigned_users_db:
            u.delete()
            for u in users_asigned:
                try:
                    AsignedUser.objects.create(
                        User = User.objects.get(username=u),
                        Issue = issue,
                        )
                except:
                    print("Ya existe")
                Activity.objects.create(
                    creator = User.objects.get(username=request.user.username),
                    issue = issue,
                    type = "assigned to",
                    user = User.objects.get(username=u)
                )    
    else:
        AsignedUser.objects.filter(Issue = issue).delete()
        

    DeadLine = request.POST.get('DeadLine')

    if(issue.Subject != subject):
        issue.Subject = subject

    if(issue.Description != descripition and descripition != 'None'):
        issue.Description = descripition
        
        Activity.objects.create(
                creator = User.objects.get(username=request.user.username),
                issue = issue,
                type = "description"
        )

    if(issue.Status != status):
        issue.Status = status

    if(issue.Type != type and type != ""):
        issue.Type = type
        
        Activity.objects.create(
                creator = User.objects.get(username=request.user.username),
                issue = issue,
                type = "type"
        )

    if(issue.Severity != severity and severity != ""):
        issue.Severity = severity
        
        Activity.objects.create(
                creator = User.objects.get(username=request.user.username),
                issue = issue,
                type = "severity"
        )

    if(issue.Priority != priority and priority != ""):
        issue.Priority = priority

        Activity.objects.create(
                creator = User.objects.get(username= request.user.username),
                issue = issue,
                type = "priority"
        )
    if(issue.DeadLine != DeadLine):
        if(DeadLine == ''):
            issue.DeadLine = None
        else :            
            issue.DeadLine = DeadLine
            Activity.objects.create(
                creator = User.objects.get(username=request.user.username),
                issue = issue,
                type = "due date"
            )

    issue.save()

    return HttpResponseRedirect('/')

@login_required(login_url='login')
@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('Comment')
        issue = request.POST.get('id')
        creator_id = User.objects.get(username=request.user.username).id
        comment_obj = {'Comment': comment,
                   'Issue': issue,
                   'Creator': creator_id}
        print(comment_obj)
        requests.post(URI+'api/comments', json = comment_obj)
        return HttpResponseRedirect('/issue/' + issue)
  


@login_required(login_url='login')
@csrf_exempt
def bulk_insert(request):
    if request.method == 'POST':
        issues = request.POST.get('issues')
        for line in issues.splitlines():
            print(line)
            issue = {'Subject': line}
            requests.post(URI+'api/issues', json = issue)

    return render(request, 'bulk_insert.html')


def remove_all_activities(request):
    Activity.objects.all().delete()
    


@login_required(login_url='login')
@csrf_exempt
def add_file(request):
    if request.method == 'POST':
        issue = request.POST.get('id')
        file = request.FILES['myfile']
        name = str(file)
        file_obj = {
            'File': file,
            'Name': name,
            'Issue': issue
        }
        print(file_obj)
        requests.post(URI+'api/files', json = file_obj)
        return HttpResponseRedirect('/issue/' + issue)

@login_required(login_url='login')
@csrf_exempt
def delete_file(request):
    id = request.POST.get('id')
    issue = request.POST.get('issue')
    AttachedFile.objects.filter(id=id).delete()
    return view_isue(request, issue)

@login_required(login_url='login')
@csrf_exempt
def block_issue_view(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST':
        issue.Block_reason = 'Blocked: ' + request.POST.get('Block_reason')
        issue.save()
        Activity.objects.create(
            creator = User.objects.get(username=request.user.username),
            issue = issue,
            type = "Blocked"
        )
        return redirect("http://127.0.0.1:8000/issue/"+str(issue_id))
    
    return render(request, 'block_issue.html')

@login_required(login_url='login')
@csrf_exempt
def desblock_issue_view(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    issue.Block_reason = None
    issue.save()
    return redirect("http://127.0.0.1:8000/issue/"+str(issue_id))

@login_required(login_url='login')
@csrf_exempt
def view_profile_view(request):
    created = Activity.objects.filter(creator = request.user)
    assigned =Activity.objects.filter(user = request.user)
    activities = created.union(assigned).order_by('created_at')

    context = {'activities': activities}
    return render(request, 'view_profile.html', context)

