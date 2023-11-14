from django.db import models
from employees.models import Employees


class Projects(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = "timesheets"
        db_table = "projects"


class Entries(models.Model):
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    description = models.TextField()
    user_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)

    @property
    def duration(self):
        if self.hours or self.minutes:
            return f"{self.hours:02d}:{self.minutes:02d}"
        return "HH:MM"
    
    @staticmethod
    def get_totals(queryset):        
        mins = sum([qs.minutes for qs in queryset])
        hours = sum([qs.hours for qs in queryset])

        return check_time(hours, mins)

    class Meta:
        app_label = "timesheets"
        db_table = "entries"



def check_time(hours, mins):
    hours += mins // 60
    mins = mins % 60
    return hours, mins