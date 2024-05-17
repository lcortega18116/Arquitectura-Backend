from ..models import Person
from django.db.models import Q


def createUser(data):
    try:
        print(data)
        Person.objects.create(**data)
        return 'created successfully'
    except Exception as e:
        print (str(e))
        return e

def readUser(request):

    params = dict(request.GET)
    fields = [field.name for field in Person._meta.get_fields()]

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
        response = Person.objects.filter(query).order_by('-id')
        if len(response) == 0:
            return 'Usuarios no registrados'
        return response

    except Exception as e:
        print(e)
        return None

  
def updateUser(id, data):
    try:
        print(data)
        # Obtener el registro que deseas actualizar
        registro = Person.objects.get(id=id)
        if registro.email != data['email']:
            return 'updated not successfully'
        
        # Actualizar los campos del registro con los valores proporcionados en el diccionario data
        for key, value in data.items():
            setattr(registro, key, value)
            
        # Guardar los cambios en la base de datos
        registro.save()
        return 'updated successfully'
    except Person.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)

def deleteUser(id):
    try:
        registro = Person.objects.filter(id=id)
        if len(registro) == 0:
            return 'deleted not successfully'
        registro.delete()
        return 'deleted successfully'
    except Person.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)
    
