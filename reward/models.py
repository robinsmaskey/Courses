from config.model_mixins import IdentifierTimeStampAbstractModel
from django.db import models


class Reward(IdentifierTimeStampAbstractModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
