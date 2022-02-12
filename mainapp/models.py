from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model as user

class Task(models.Model):
    user = models.ForeignKey(user(), on_delete=models.CASCADE)
    task = models.CharField(verbose_name=_("Task"), max_length=100)
    added_date = models.DateTimeField(verbose_name=_("Creation date"), default=timezone.now)
    due_date = models.DateField(null=True, blank=True, verbose_name=_("Due date"))
    completed = models.BooleanField(default=False, verbose_name=_("Task completion"))

    def __str__(self):
        if len(self.task) > 20:
            task_name = self.task[0:20] + '...'
        else:
            task_name = self.task
        return f"{task_name} created: {self.added_date}"
    
    def is_due_date_passed(self):
        if self.due_date != None and self.due_date < timezone.now().date():
            return True
        return False

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        