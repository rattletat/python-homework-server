from django.db import models
from django.utils.timezone import now


class Exercise(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True, default=None)
    release = models.DateTimeField(null=True, default=None)
    deadline = models.DateTimeField(null=True, default=None)

    def is_started(self):
        if self.release:
            return self.release < now()
        else:
            return True

    def is_finished(self):
        if self.deadline:
            return self.deadline < now()
        else:
            return False
