import datetime

from timesheets.models import Projects, Entries


def get_weekly_table(user_id, week_num):    
    entries = Entries.objects.filter(user_id=user_id)
    projects = Projects.objects.filter(active=True) 

    week = get_week(week_num)  
    entries_in_week = entries.filter(date__in=week)
    
    totals_by_date = []
    for day in week:
        hours, mins = Entries.get_totals(entries_in_week.filter(date=day))
        totals_by_date.append(f"{hours:02d}:{mins:02d}")

    project_data = []
    projects_in_week = projects.filter(pk__in=[entry.project_id.id for entry in entries_in_week])
    for project in projects_in_week:
        entries_in_project = entries_in_week.filter(project_id=project.id)
        hours, mins = Entries.get_totals(entries_in_project)
        data = {
            "id": project.id,
            "name": project.name,
            "totals": f"{hours:02d}:{mins:02d}",
            "entries": []
        }

        for day in week:
            entry = entries_in_project.filter(date=day).first()
            if entry:
                data["entries"].append({
                    "id": entry.id,
                    "hours": entry.hours,
                    "minutes": entry.minutes,
                    "description": entry.description,
                    "user_id": entry.user_id.id,
                    "user_name": entry.user_id.name,
                    "project_id": entry.project_id.id,
                    "project_name": entry.project_id.name,
                    "date": entry.date,
                    "duration": entry.duration,
                })
            else:
                data["entries"].append({})

        project_data.append(data)

    return {
        "projects": project_data,
        "totals_by_date": totals_by_date,
        "week": week
    }


def get_week(week=0):    
    current_day = datetime.date.today() + datetime.timedelta(weeks=int(week))
    week = [current_day + datetime.timedelta(days=i) for i in range(0 - current_day.weekday(), 7 - current_day.weekday())]
    week.sort(key=lambda day: day.weekday())
    return week

