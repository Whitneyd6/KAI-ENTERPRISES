from django.db import models

# Create your models here.
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='equipment',
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'equipment'
        ordering = ['department', 'name']

    def __str__(self):
        return f'{self.name} ({self.department.name})'    