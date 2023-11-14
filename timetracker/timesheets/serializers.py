from rest_framework import serializers

from .models import Projects, Entries, check_time


class EntriesSerializer(serializers.ModelSerializer):

    def validate(self, data):
        entries = Entries.objects.all()
        errors = []

        entries_in_date = entries.filter(user_id=data["user_id"], date=data["date"])
        hours, mins = Entries.get_totals(entries_in_date)
        print(data)
        total_hours, total_mins = check_time(hours + data.get("hours", 0), mins + data.get("minutes", 0))
        if total_hours > 24:
            errors.append("There are only 24 hours within a day")
        if total_mins > 60:
            errors.append("There are only 60 minutes within an hour")

        data["hours"], data["minutes"] = check_time(data.get("hours", 0), data.get("minutes", 0))

        if errors:
            raise serializers.ValidationError(errors)
        
        return super().validate(data)
    
    def create(self, data):        
        entries = Entries.objects.all()
        errors = []

        existing = entries.filter(user_id=data["user_id"], date=data["date"], project_id=data["project_id"])
        if existing:
            errors.append("Entry already exists")
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return super().create(data)

    class Meta:
        model = Entries
        fields = "__all__"


class ProjectsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = "__all__"

