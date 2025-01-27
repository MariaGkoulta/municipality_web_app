# Generated by Django 3.1.1 on 2020-09-23 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('release_date', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('comments', models.CharField(max_length=20)),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('direction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.direction')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('activity_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='municipality_project.activity')),
                ('numberOfTasks', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('deptid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.department')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shown', models.BooleanField(default=False)),
                ('date', models.DateTimeField()),
                ('message', models.TextField()),
                ('activity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.activity')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.employee')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='direction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.direction'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('sentBySender', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('activity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.activity')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.employee'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('activity_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='municipality_project.activity')),
                ('approved', models.BooleanField(default=False)),
                ('isDivided', models.BooleanField(default=False)),
                ('project_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='municipality_project.project')),
                ('receiver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.employee')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='motherTask',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='the_mother_task+', to='municipality_project.activity'),
        ),
        migrations.CreateModel(
            name='OfficeClerk',
            fields=[
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='municipality_project.employee')),
                ('deptid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.department')),
                ('officeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.office')),
            ],
        ),
        migrations.CreateModel(
            name='DeptDirector',
            fields=[
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='municipality_project.employee')),
                ('deptid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipality_project.department')),
            ],
        ),
    ]
