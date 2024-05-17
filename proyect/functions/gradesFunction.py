from ..models import Grade
from django.db.models import Q


def createGrade(data):
    try:
        print(data)
        Grade.objects.create(**data)
        return 'created successfully'
    except Exception as e:
        print (str(e))
        return e

def readGrade(request):

    params = dict(request.GET)
    fields = [field.name for field in Grade._meta.get_fields()]

    # Check the fields 
    for p in params: 
        if p not in fields: 
            return "Field {} not found".format(p)

    final_fields = {}
    for f in fields:
        final_fields[f] = request.GET.get(f,'')
    print(final_fields)
    
    query = Q()
    for key, value in final_fields.items():
        if value != '':
            query &= Q(**{key: value})
    
    try:    
        response = Grade.objects.filter(query).order_by('-id')
        if len(response) == 0:
            return 'not found'
        return response

    except Exception as e:
        print(e)
        return None

  
def updateGrade(id, data):
    try:
        print(data)
        # Obtener el registro que deseas actualizar
        registro = Grade.objects.get(id=id)
        if registro.student_id != data['student_id']:
            return 'updated not successfully'
        if registro.class_code != data['class_code']:
            return 'updated not successfully'
        
        # Actualizar los campos del registro con los valores proporcionados en el diccionario data
        for key, value in data.items():
            setattr(registro, key, value)
            
        # Guardar los cambios en la base de datos
        registro.save()
        return 'updated successfully'
    except Grade.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)

def deleteGrade(id):
    try:
        registro = Grade.objects.filter(id=id)
        if len(registro) == 0:
            return 'deleted not successfully'
        registro.delete()
        return 'deleted successfully'
    except Grade.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)
    
