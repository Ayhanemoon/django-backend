from django.db import models


class AddressQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)


class AddressManager(models.Manager):
    def get_queryset(self):
        return AddressQuerySet(self.model, using=self._db)

    def alive(self):
        return self.get_queryset().alive()

    def deleted(self):
        return self.get_queryset().deleted()
