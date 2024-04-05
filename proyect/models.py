from django.db import models

# Create your models here.
        
class person(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.TextField(blank=True, null=False)
    lastname = models.TextField(blank=True, null=False)
    role = models.TextField(blank=True, null=False)
    email = models.TextField(blank=True, null=False)
    password = models.TextField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'person'
        # unique_together = (('database_id', 'categoria', 'codigo','indicexcodigo'),)