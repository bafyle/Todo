from django.contrib.auth import get_user_model as user
from django.db.models import Q

from django.utils import timezone

class Job():
    help = "Delete all users that haven't been active for more than 30 days"

    def execute(self):
        users = user().objects.filter(Q(last_login=None) | Q(last_login__lte = timezone.now()-timezone.timedelta(days=30)))
        for u in users:
            if u.last_login == None:
                if u.date_joined <= timezone.now()-timezone.timedelta(days=30):
                    u.delete()
            u.delete()

