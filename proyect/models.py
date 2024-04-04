from django.db import models

# Create your models here.
    
class TWmsVinculos(models.Model):
    database_id = models.CharField(max_length=20, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.CharField(max_length=255, blank=True, null=True)
    indicexcodigo = models.IntegerField(blank=True, null=True)
    hipervinculo = models.TextField(blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 't_wms_vinculos'
        
class person(models.Model):
    id = models.AutoField(primary_key=True)
    fisrtname = models.TextField(blank=True, null=False)
    lastname = models.TextField(blank=True, null=False)
    role = models.TextField(blank=True, null=False)
    email = models.TextField(blank=True, null=False)
    password = models.TextField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'person'
        # unique_together = (('database_id', 'categoria', 'codigo','indicexcodigo'),)