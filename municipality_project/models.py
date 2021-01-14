from django.db import models

class Direction(models.Model):
    name = models.CharField(max_length=200)

class Employee(models.Model):
    employee_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    direction_id = models.ForeignKey(Direction, on_delete=models.CASCADE)

class Activity(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True)
    release_date = models.DateTimeField()
    deadline = models.DateTimeField()
    comments = models.CharField(max_length=20, blank=True)
    complete = models.BooleanField(default=False)
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE)

class Notification(models.Model):
    activity_id = models.ForeignKey(Activity, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shown = models.BooleanField(default=False)
    date = models.DateTimeField()
    message = models.TextField()

class Comment(models.Model):
    message = models.TextField()
    sentBySender = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    activity_id = models.ForeignKey(Activity, on_delete=models.CASCADE)

class Project(models.Model):
    activity_id = models.OneToOneField(Activity, on_delete=models.CASCADE, primary_key=True)
    numberOfTasks = models.IntegerField(blank=True)
    motherTask = models.ForeignKey(Activity, on_delete=models.SET_NULL, blank=True, null=True, related_name='the_mother_task+')

class Task(models.Model):
    activity_id = models.OneToOneField(Activity, on_delete=models.CASCADE, primary_key=True)
    receiver_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default = False)
    isDivided = models.BooleanField(default = False)

class Department(models.Model):
    name = models.CharField(max_length=200)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)

class Office(models.Model):
    name = models.CharField(max_length=200)
    deptid = models.ForeignKey(Department, on_delete=models.CASCADE)

class DeptDirector(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    deptid = models.ForeignKey(Department, on_delete=models.CASCADE)

class OfficeClerk(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    deptid = models.ForeignKey(Department, on_delete=models.CASCADE)
    officeid = models.ForeignKey(Office, on_delete=models.CASCADE)
