from ..models import TWmsVinculos
from django.db.models import Q

def create_Vinculo(data):
    try:
        print(data)
        TWmsVinculos.objects.using('S3').create(**data)
        return 'created successfully'
    except Exception as e:
        return e

# def read_Vinculo(database_id,categoria,codigo):
#     try:
#         registros = TWmsVinculos.objects.using('default').filter(database_id=database_id,categoria=categoria,codigo=codigo)
#         return registros
#     except TWmsVinculos.DoesNotExist:
#         return 'Registro no encontrado'
#     except Exception as e:
#         return str(e)
def read_Vinculo(request,database_id, db_name):

    params = dict(request.GET)
    fields = [field.name for field in TWmsVinculos._meta.get_fields()]

    # Check the fields 
    for p in params: 
        if p not in fields: 
            return "Field {} not found".format(p)

    final_fields = {}
    for f in fields:
        if f == "database_id":
            final_fields[f] = database_id
        else:
            final_fields[f] = request.GET.get(f,'')
    print(final_fields)
    
    query = Q()
    for key, value in final_fields.items():
        if value != '':
            query &= Q(**{key: value})
    
    
    try:    
        response = TWmsVinculos.objects.using('S3').filter(query).order_by('-id')
        if len(response) == 0:
            return 'No hay imagenes registradas'
        return response

    except Exception as e:
        print(e)
        return None

  
def update_Vinculo(id, data):
    try:
        # Obtener el registro que deseas actualizar
        registro = TWmsVinculos.objects.using('S3').get(id=id)
        if registro.database_id != data['database_id']:
            return 'updated not successfully'
        # Actualizar los campos del registro con los valores proporcionados en el diccionario data
        for key, value in data.items():
            setattr(registro, key, value)

        # Guardar los cambios en la base de datos
        registro.save()

        return 'updated successfully'
    except TWmsVinculos.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)

def delete_Vinculo(id,database_id):
    try:
        registro = TWmsVinculos.objects.using('S3').get(id=id)
        if registro.database_id != database_id:
            return 'deleted not successfully'
        registro.delete()
        return 'deleted successfully'
    except TWmsVinculos.DoesNotExist:
        return 'item not found'
    except Exception as e:
        return str(e)
    
def maxid_Vinculo(codigo,categoria,database_id):
    try:
        registro = TWmsVinculos.objects.using('S3').filter(codigo=codigo,categoria=categoria,database_id=database_id).order_by('-indicexcodigo')[0]
        if registro:
            return str(registro.indicexcodigo+1)
        else:
            return '0'
    except Exception as e:
        print (str(e))
        return '0'
