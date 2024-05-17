from ..models import Presence
from django.db.models import Q


def createPresence(data):
    try:
        print(data)
        Presence.objects.create(**data)
        return 'created successfully'
    except Exception as e:
        print (str(e))
        return e

def readPresence(request):

    params = dict(request.GET)
    fields = [field.name for field in Presence._meta.get_fields()]

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
        response = Presence.objects.filter(query).order_by('-id')
        if len(response) == 0:
            return 'not found'
        return response

    except Exception as e:
        print(e)
        return None

  
def updatePresence(id, data):
    try:
        print(data)
        # Obtener el registro que deseas actualizar
        registro = Presence.objects.get(id=id)
        if registro.teacher_id != data['teacher_id']:
            return 'updated not successfully'
        if registro.student_id != data['student_id']:
            return 'updated not successfully'
        
        # Actualizar los campos del registro con los valores proporcionados en el diccionario data
        for key, value in data.items():
            setattr(registro, key, value)
            
        # Guardar los cambios en la base de datos
        registro.save()
        return 'updated successfully'
    except Presence.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)

def deletePresence(id):
    try:
        registro = Presence.objects.filter(id=id)
        if len(registro) == 0:
            return 'deleted not successfully'
        registro.delete()
        return 'deleted successfully'
    except Presence.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)
    
