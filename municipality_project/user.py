from municipality_project.models import Employee, Task, OfficeClerk, DeptDirector
from municipality_project.context_processors import get_logged_user

# with this method, we get the subordinates of an employee
def get_subs(employee):
    try :
        deptDirector = DeptDirector.objects.get(employee_id=employee.employee_id)
        subs = OfficeClerk.objects.filter(deptid = deptDirector.deptid).select_related('employee')
    except (KeyError, DeptDirector.DoesNotExist):
        try :
            officeClerk = OfficeClerk.objects.get(employee_id=employee.employee_id)
        except (KeyError, OfficeClerk.DoesNotExist):
            subs = Employee.objects.filter(direction_id=employee.direction_id)
    return subs
