from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import requests

from issues.serializers import AttachedFileSerializer
from .models import AsignedUser, Issue, Activity, Watcher, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Issue
from .models import AttachedFile
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response




# Create your views here.import requests




@login_required(login_url='login')
def view_isue(request, issue_id):
    #Crida a la api per a obtenir tots els comments del issue

    files = requests.get(settings.BASE_URL + '/api/files?id=' + str(issue_id))
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

    try:
        comments = Comment.objects.filter(Issue = issue).order_by('-Created_at')
    except Http404:
        print('No tiene comments')

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
               'comments': comments,
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


    Activity.objects.filter(issue = issue, type = "watches").delete()
    Activity.objects.filter(issue = issue, type = "assigned to").delete()


    print('-------------------------- Borrado:')
    print(len(Activity.objects.all()))

    if(len(watchers) > 0):
        for w in watchers_db:
            w.delete()
        for w in watchers:
            try:
                Watcher.objects.create(
                    User = User.objects.get(username = w),
                    Issue = issue,
                )
            except:
                print("Ya existe")
            Activity.objects.create(
                    creator = User.objects.get(username=request.user.username),
                    issue = issue,
                    type = "watches",
                    user = User.objects.get(username=w)
            )    
        print('CREADO')
    else:
        Watcher.objects.filter(Issue = issue).delete()


    if(len(users_asigned) > 0):
        print(len(users_asigned))
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
            print('----------------------------')
            print(request.user.username + ' ' + u)    
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

    return HttpResponseRedirect(settings.BASE_URL)


def remove_all_activities(request):
    Activity.objects.all().delete()

@login_required(login_url='login')
@csrf_exempt
def view_profile_view(request):
    created = Activity.objects.filter(creator = request.user)
    assigned =Activity.objects.filter(user = request.user)
    activities = created.union(assigned).order_by('created_at')

    context = {'activities': activities,
               'base_url': settings.BASE_URL}
    return render(request, 'view_profile.html', context)


@login_required(login_url='login')
@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def file(request):
    if request.method == 'GET':
        file = AttachedFile.objects.get(id = request.AttachedFile.id)
        serializer = AttachedFileSerializer(file)
        return Response(serializer.data)
    
    if request.method == 'POST':
        issue_id = request.data.get('Issue')

        try:
            issue = Issue.objects.get(id=int(issue_id))
            file = request.FILES.get('File')

            attachedFile = AttachedFile()
            attachedFile.Issue = issue
            attachedFile.File = file
            attachedFile.Name = str(file)

            try:
                attachedFile.save()
            except:
                return Response({'error': 'Al crear el archivo'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)
        
        except Issue.DoesNotExist():
            return Response({'error': 'El issue con id \'' + issue_id + '\' no esitse'} , status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        id = request.POST.get('id')
        try:
            AttachedFile.objects.filter(id=id).delete()
            return Response({'success': True, 'message': 'File deleted'})
        except:
            return Response({'error': 'El file con id \'' + id + '\' no esitse'} , status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='login')
@api_view(['PUT'])
@csrf_exempt
def toggle_block_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'PUT':
        if request.PUT.get('Block_reason') == None:            
            issue.Block_reason = None
            issue.save()
            return Response({'success': True, 'message': 'Issue desblocked'})
        
        else:
            issue.Block_reason = 'Blocked: ' + request.POST.get('Block_reason')
            issue.save()
            try:
                Activity.objects.create(
                    creator = User.objects.get(username=request.user.username),
                    issue = issue,
                    type = "Blocked"
                )
            except:
                return Response({'error': 'Al crear el activity'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': True, 'message': 'Issue blocked'})
