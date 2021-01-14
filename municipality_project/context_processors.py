import datetime, locale
from municipality_project.models import Employee, Task, OfficeClerk, DeptDirector

def get_current_year_to_context(request):
    current_datetime = datetime.date.today()
    return {
        'current_date': current_datetime.strftime("%d/%m/%Y")
    }

def get_logged_user(request):
    dirDirector = None
    try:
        employee = Employee.objects.get(employee_id=request.session['logged_employee'])
        try :
            deptDirector = DeptDirector.objects.get(employee_id=employee.employee_id)
        except (KeyError, DeptDirector.DoesNotExist):
            deptDirector = None
        try :
            officeClerk = OfficeClerk.objects.get(employee_id=employee.employee_id)
        except (KeyError, OfficeClerk.DoesNotExist):
            officeClerk = None
        if not (officeClerk or deptDirector):
            dirDirector = employee
    except (KeyError, Employee.DoesNotExist):
        employee = None
        deptDirector = None
        officeClerk = None
    return {
        'employee': employee,
        'dirDirector': dirDirector,
        'deptDirector': deptDirector,
        'officeClerk': officeClerk
}
