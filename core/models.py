from datetime import datetime

from django.db import models
from django.utils import timezone

date_today = timezone.now()


# Create your models here.
class AbstractBaseModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class PlatformLog(AbstractBaseModel):
    actioned_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    action = models.JSONField(default=list)
