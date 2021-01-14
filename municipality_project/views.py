from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from municipality_project.models import Employee, Task, Activity, Project, Notification
from django.contrib.auth import logout
from municipality_project.context_processors import get_logged_user
from municipality_project.user import get_subs
from django.urls import reverse
import datetime
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json

def login(request):
    return render(request, 'municipality_project/login.html')

def logout(request):
    request.session['logged_employee'] = None
    return render(request, 'municipality_project/logout.html')

def authenticate(request):
        username = request.POST['username']
        password = request.POST['password']
        if ((username == "") or (password == "")):
            context = {
            'errors': 'Παρακαλώ συμπληρώστε όλα τα πεδία ώστε να συνεχίσετε.'
            }
            return render(request, 'municipality_project/login.html', context)
        employee = Employee.objects.filter(employee_id=username, password=password)
        if employee:
            emp = employee[0]
            request.session['logged_employee'] = emp.employee_id
            logged_user = get_logged_user(request)
            if (not (logged_user['officeClerk'] or logged_user['deptDirector'])):
                context = {
                'employee': emp,
                'activities': Activity.objects.filter(sender=emp.employee_id)
                }
                return render(request, 'municipality_project/activities.html', context)
            else:
                context = my_tasks_context(request)
                return render(request, 'municipality_project/mytasks.html', context)
        else:
            context = {
            'errors': 'Λανθασμένο όνομα χρήστη ή κωδικός πρόσβασης. Παρακαλώ προσπαθήστε ξανά.'
            }
            return render(request, 'municipality_project/login.html', context)

def my_tasks_context(request):
    logged = get_logged_user(request)
    emp = logged['employee']
    tasks = Task.objects.filter(receiver_id=emp.employee_id).select_related('activity_id').order_by('activity_id__deadline')
    numberOfTasks = len(tasks)
    context = {
        'employee': emp,
        'tasks': tasks,
        'numberOfTasks': numberOfTasks
    }
    return context

def my_tasks(request):
    logged = get_logged_user(request)
    emp = logged['employee']
    if (emp):
        if (logged['officeClerk'] or logged['deptDirector']):
            context = my_tasks_context(request)
            return render(request, 'municipality_project/mytasks.html', context)
        else:
            return render(request, 'municipality_project/login.html')
    else:
        context = {
        'errors': 'Για να έχετε πρόσβαση σε αυτή τη σελίδα παρακαλώ συνδεθείτε.'
        }
        return render(request, 'municipality_project/login.html', context)

def activities_view(request):
    logged = get_logged_user(request)
    emp = logged['employee']
    if logged['deptDirector'] or logged['dirDirector']:
        activities = Activity.objects.filter(sender=emp.employee_id).order_by('deadline')
        context = {
        'activities': activities,
        }
        return render(request, 'municipality_project/activities.html', context)
    else:
        return render(request, 'municipality_project/login.html')

def create_activity(request):
    logged = get_logged_user(request)
    if logged['officeClerk']:
        return my_tasks(request)
    else:
        return render(request, 'municipality_project/create_activity.html')

def create_task(request):
    logged = get_logged_user(request)
    emp = logged['employee']
    if logged['officeClerk']:
        return my_tasks(request)
    subs = get_subs(emp)
    context = {
    'employee': emp,
    'subs': subs
    }
    return render(request, 'municipality_project/create_task.html', context)

def save_task(request):
    task_title = request.POST['title']
    task_deadline = request.POST['date']
    task_description = request.POST['description']
    receiver_id = request.POST['receiver']
    receiver = Employee.objects.get(employee_id=receiver_id)
    new_activity = Activity(title=task_title, description = task_description, release_date=datetime.date.today(), deadline=task_deadline, sender=get_logged_user(request)['employee'])
    new_task = Task(activity_id = new_activity, receiver_id=receiver)
    not_message = "Ο χρήστης "+get_logged_user(request)['employee'].name+ " "+ get_logged_user(request)['employee'].surname +" σας ανέθεσε την αρμοδιότητα "+ task_title
    new_notification = Notification(activity_id=new_activity, receiver=receiver, date=datetime.date.today(), message=not_message)
    new_activity.save()
    new_task.save()
    new_notification.save()
    return activities_view(request)

def activity_view(request, activity_id):
    try:
        activity = Activity.objects.get(pk=activity_id)
    except (KeyError, Activity.DoesNotExist):
        context = {
        'errors': "Η δραστηριότητα δε βρέθηκε!",
        }
        return render(request, 'municipality_project/taskRow.html', context)
    try:
        task = Task.objects.get(activity_id=activity)
        context = {
        'activity': activity,
        'task': task,
        }
        return render(request, 'municipality_project/taskRow.html', context)
    except (KeyError, Task.DoesNotExist):
        project = Project.objects.get(activity_id=activity)
        project_tasks = Task.objects.filter(project_id = project).select_related('activity_id')
        context = {
        'activity': activity,
        'project':project,
        'project_tasks':project_tasks
        }
        return render(request, 'municipality_project/projectRow.html', context)

def create_project(request):
    logged = get_logged_user(request)
    if logged['officeClerk']:
        return my_tasks(request)
    else:
        return render(request, 'municipality_project/create_project.html')

def project_task(request):
    if not ('activities' in request.session):
        request.session['activities'] = []
        request.session['tasks'] = []
    project_title = request.POST['project_title']
    project_deadline = request.POST['project_deadline']
    project_description = request.POST['project_description']
    logged = get_logged_user(request)
    emp = logged['employee']
    subs = get_subs(emp)
    context = {
    'employee': emp,
    'subs': subs,
    'project_title':project_title,
    'project_deadline':project_deadline,
    'project_description':project_description,
    }
    return render(request, 'municipality_project/create_project_task.html', context)

def save_project(request):
    project_title = request.POST['project_title']
    project_deadline = request.POST['project_deadline']
    project_description = request.POST['project_description']
    new_project_activity = Activity(title=project_title, description = project_description, release_date=datetime.date.today(), deadline=project_deadline, sender=get_logged_user(request)['employee'])
    task_title = request.POST['title']
    task_deadline = json.dumps(request.POST['date'])
    task_description = request.POST.get('description', "")
    receiver_id = request.POST['receiver']
    done = request.POST.get('done', False)
    next = request.POST.get('next', False)
    new_activity = []
    new_task = []
    activities = request.session['activities']
    tasks = request.session['tasks']
    new_activity.append((task_title, task_description, task_deadline))
    activities.append(new_activity)
    new_task.append((new_activity, receiver_id))
    tasks.append(new_task)
    request.session['activities'] = activities
    request.session['tasks'] = tasks

    if (next):
        return project_task(request)
    if (done):
        new_project_activity.save()
        new_project = Project(activity_id=new_project_activity, numberOfTasks = len(activities))
        new_project.save()
        for i in range(len(activities)):
            request.session['activities'] = []
            request.session['tasks'] = []
            new_activity_obj = Activity(title=activities[i][0][0], description = activities[i][0][1], release_date=datetime.date.today(), deadline=json.loads(activities[i][0][2]), sender=get_logged_user(request)['employee'])
            new_activity_obj.save()
            receiver = Employee.objects.get(employee_id=tasks[i][0][1])
            new_task_obj = Task(activity_id=new_activity_obj, receiver_id=receiver, project_id = new_project)
            new_task_obj.save()
            not_message = "Ο χρήστης "+get_logged_user(request)['employee'].name+ " "+ get_logged_user(request)['employee'].surname +" σας ανέθεσε την αρμοδιότητα "+ activities[i][0][0]
            new_notification = Notification(activity_id=new_activity_obj, receiver=receiver, date=datetime.date.today(), message=not_message)
            new_notification.save()
        return activities_view(request)

def notifications_view(request):
    logged = get_logged_user(request)
    emp = logged['employee']
    notifications = Notification.objects.filter(receiver=emp).select_related('activity_id')
    context = {
        'notifications' : notifications,
    }
    return render(request, 'municipality_project/notifications.html', context)

def completeTask_view(request):
    activity_id = request.POST['selectedTasks']
    activity = Activity.objects.get(pk=activity_id)
    activity.complete = True
    activity.save()
    return my_tasks(request)

def info(request):
   return render(request, 'municipality_project/info.html')
