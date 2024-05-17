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
    id_teacher = models.ForeignKey('Person', models.DO_NOTHING, db_column='id_teacher')
    start_date = models.DateField()
    finish_date = models.DateField()
    start_time = models.TimeField()
    finish_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'class'

class Grade(models.Model):
    student_id = models.ForeignKey('Person', models.DO_NOTHING)
    class_code = models.ForeignKey(Class, models.DO_NOTHING, db_column='class_code')
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    percent = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'grade'

class Presence(models.Model):
    class_code = models.ForeignKey(Class, models.DO_NOTHING, db_column='class_code')
    student_id = models.ForeignKey(Person, models.DO_NOTHING)
    register_date = models.DateTimeField()
    teacher_id = models.ForeignKey(Person, models.DO_NOTHING, related_name='presence_teacher_set')

    class Meta:
        managed = False
        db_table = 'presence'

        # unique_together = (('database_id', 'categoria', 'codigo','indicexcodigo'),)