from ..models import Class
from django.db.models import Q


def createClass(data):
    try:
        print(data)
        Class.objects.create(**data)
        return 'created successfully'
    except Exception as e:
        print (str(e))
        return e

def readClass(request):

    params = dict(request.GET)
    fields = [field.name for field in Class._meta.get_fields()]

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
        response = Class.objects.filter(query).order_by('-code')
        if len(response) == 0:
            return 'not found'
        return response

    except Exception as e:
        print(e)
        return None

  
def updateClass(code, data):
    try:
        print(data)
        # Obtener el registro que deseas actualizar
        registro = Class.objects.get(code=code)
        if registro.id_teacher != data['id_teacher']:
            return 'updated not successfully'
        
        # Actualizar los campos del registro con los valores proporcionados en el diccionario data
        for key, value in data.items():
            setattr(registro, key, value)
            
        # Guardar los cambios en la base de datos
        registro.save()
        return 'updated successfully'
    except Class.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)

def deleteClass(code):
    try:
        registro = Class.objects.filter(code=code)
        if len(registro) == 0:
            return 'deleted not successfully'
        registro.delete()
        return 'deleted successfully'
    except Class.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)
    
