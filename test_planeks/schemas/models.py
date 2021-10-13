from django.contrib.auth.models import User
from django.db import models

class Schema(models.Model):

    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    all_column = []

    class Meta:

        ordering = ('updated', )
        verbose_name = 'schema'
        verbose_name_plural = 'schemas'

class Column(models.Model):

    title = models.CharField(max_length=50)

    LOAN_STATUS = (
        ('n', 'Name'),
        ('c', 'Company'),
        ('e', 'E-mail'),
        ('a', 'Adress'),
        ('r', 'Reserved'),
    )

    order = models.IntegerField()
    type = models.CharField(max_length=50)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def get_absolute_url(self):

        return f'/schema/{self.schema_id}'



    class Meta:

        ordering = ('order',)
        verbose_name = 'column'
        verbose_name_plural = 'columns'
