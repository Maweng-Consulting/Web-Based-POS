from django.db import models


# Create your models here.
class AbstractBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


class PlatformLog(AbstractBaseModel):
    actioned_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    action = models.JSONField(default=list)