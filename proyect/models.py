from django.db import models

# Create your models here.
        
class Person(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.TextField(blank=True, null=False)
    lastname = models.TextField(blank=True, null=False)
    role = models.TextField(blank=True, null=False)
    email = models.TextField(blank=True, null=False)
    password = models.TextField(blank=True, null=False)
    status = models.IntegerField(blank=True, null=False)
    
    class Meta:
        managed = False
        db_table = 'person'

class Class(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    id_teacher = models.IntegerField()
    start_date = models.DateField()
    finish_date = models.DateField()
    start_time = models.TimeField()
    finish_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'class'

class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.IntegerField()
    class_code = models.IntegerField()
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    percent = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'grade'

class Presence(models.Model):
    class_code = models.IntegerField()
    student_id = models.IntegerField()
    teacher_id = models.IntegerField()
    register_date = models.DateTimeField()
    

    class Meta:
        managed = False
        db_table = 'presence'

        # unique_together = (('database_id', 'categoria', 'codigo','indicexcodigo'),)