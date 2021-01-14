import datetime
from django import template
from municipality_project.models import Employee, Task, Activity, DeptDirector, OfficeClerk, Notification, Direction, Department, Office

register = template.Library()

@register.filter(name='isTask')
def isTask(activity):
    if Task.objects.filter(activity_id=activity).exists():
        return True
    else:
        return False

@register.filter(name='isApproved')
def isApproved(activity):
    tasks = Task.objects.filter(activity_id=activity)
    for task in tasks:
        if task.approved:
            return True
        else:
            return False

@register.filter(name='isNotDirectionDirector')
def isNotDirectionDirector(employee):
    isDeptDirector = DeptDirector.objects.filter(employee_id = employee.employee_id)
    isOfficeClerk = OfficeClerk.objects.filter(employee_id = employee.employee_id)
    if isOfficeClerk or isDeptDirector:
        return True
    else:
        return False

@register.filter(name='isComplete')
def isComplete(task):
    if task.approved:
        return "Ναι"
    else:
        return "Όχι"

@register.filter(name='isActivityComplete')
def isActivityComplete(activity):
    if activity.complete:
        return "Ναι"
    else:
        return "Όχι"

@register.filter(name='finishedPercentage')
def finishedPercentage(project):
    count = 0
    finishedTasks = 0
    project_tasks = Task.objects.filter(project_id = project).select_related('activity_id')
    for task in project_tasks:
        count = count + 1
        if task.approved:
            finishedTasks = finishedTasks + 1
    return (finishedTasks/count)*100

@register.filter(name='isNotDeptDirector')
def isNotDeptDirector(employee):
    isDeptDirector = DeptDirector.objects.filter(employee_id = employee.employee_id)
    if isDeptDirector:
        return False
    else:
        return True

@register.filter(name='get_activity')
def get_activity(notification):
    return Activity.objects.get(pk=notification.activity_id)

@register.filter
def finishedPercentage_to_str(project):
    value = finishedPercentage(project)
    """converts int to string"""
    return str(value)

@register.filter
def formatDate(date):
    date = date.replace(hour=0, minute=0, second=0, microsecond=0) # Returns a copy
    date = date.strftime('%d/%m/%Y')
    return date

@register.filter
def numberOfTasks(employee):
    count = 0
    tasks_query = Task.objects.filter(receiver_id=employee).select_related('activity_id')
    for task in tasks_query:
        if task.activity_id.complete:
            count = count + 1
    return len(tasks_query) - count

@register.filter
def numberOfNotifications(employee):
    not_query = Notification.objects.filter(receiver=employee)
    return len(not_query)

@register.filter
def numberOfAssigned(employee):
    activities_query = Activity.objects.filter(sender=employee)
    return len(activities_query)

@register.filter
def getDirection(employee):
    direction = Direction.objects.get(pk=employee.direction_id.pk)
    return direction.name

@register.filter
def getDepartment(employee):
    dept = Department.objects.get(pk=employee.deptid.pk)
    return dept.name

@register.filter
def getOffice(employee):
    office = Office.objects.get(pk=employee.officeid.pk)
    return office.name
