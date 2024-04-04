from django.views.decorators.csrf import csrf_exempt
import os
from io import BytesIO
from django.http.response import JsonResponse
from models import TWmsVinculos
from proyect.functions.functions import *
import json
import boto3
import rembg
from django.http import HttpResponse
import mimetypes
from dotenv import load_dotenv

load_dotenv()

@csrf_exempt
def crdVinculos(request):
    print (request._body)
    try:
        request_data = request._body
        database = request_data['database']
  
    except Exception as e:
        return JsonResponse({'message': 'Error'}, safe=False, status=500)
    db_name = 'S3'
    # Get products
    if request.method == 'GET':
        print ('GET')

        try:
            # response = read_Vinculo(database_id=database_id,categoria=categoria,codigo=codigo)
            response = read_Vinculo(request,database, db_name)
            if type(response) == str:
                return JsonResponse({'message': response}, status=204)
            else:
                if len(response) == 0:
                    return JsonResponse({'message': 'No hay imagenes registradas'}, safe=False, status=204) 
                response_json = list(response.values())
                return JsonResponse(response_json, safe=False, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': e}, safe=False, status=500)

  # Create a new article
    if request.method == 'POST':
        
        database = request_data['database'] if 'database' in request_data else None
        hipervinculo =  request_data['hipervinculo'] if 'hipervinculo' in request_data else None
        categoria = request.POST.get('categoria')
        codigo = request.POST.get('codigo')
        
        if categoria is None and codigo is None:
            return JsonResponse({'message': 'Some fields are missing'}, safe=False, status=400)
        try:
            indicexcodigo = maxid_Vinculo(codigo,categoria,database)
            print (database,categoria,codigo,indicexcodigo,hipervinculo)
        except Exception as e:
            print(e)
            return JsonResponse({'message': e}, safe=False, status=500)
        #obtener imagen de la peticion
        try:
            file = request.FILES.get('archivo')
            if file:
                uploaded_image =file.read()
                file_extension = file.name.split('.')[-1]
            else:
                print ('No file')
                return JsonResponse({'message': 'No file'}, status=400)
        except Exception as e:
            print(e)
            print ('No file')
            return JsonResponse({'message': 'No file'}, status=400)
        
        # Configura las credenciales y la región de AWS
        s3 = boto3.client('s3', aws_access_key_id=os.getenv("aws_access_key_id"), aws_secret_access_key='LPsTraFqgII7gxVmwj/m6LSfJ+cIgG51HqMdxcyf', region_name='us-east-1')  # Reemplaza 'us-east-1' con la región correcta
        
        
        archivo_s3 = f'images/{database}/{categoria}/{codigo}_{indicexcodigo}.{file_extension}'
        
        try:
            # Sube el archivo a S3
            s3.upload_fileobj(BytesIO(uploaded_image), 'sgv-filemanager-images', archivo_s3)
            # s3.upload_file(uploaded_image, 'sgv-filemanager-images', archivo_s3)
            # Genera una URL de acceso público a la imagen cargada
            hipervinculo = f'https://s3.amazonaws.com/sgv-filemanager-images/{archivo_s3}'
        except Exception as e:
            print (str(e))
            return JsonResponse({'message': 'Error al subir imagen a S3'}, status=400)
            
        data = {} 
        if database is None or categoria is None or codigo is None or indicexcodigo is None or hipervinculo is None:
            return JsonResponse({'message': 'Some fields are missing'}, safe=False, status=400)
        else:
            data['database_id'] = database
            data['categoria'] = categoria
            data['codigo'] = codigo
            data['indicexcodigo'] = indicexcodigo
            data['hipervinculo'] = hipervinculo
            
        try:
            # response = 'created successfully's
            response = create_Vinculo(data)
            if response == 'created successfully':
                return JsonResponse({'url': hipervinculo}, safe=False, status=200)

        except Exception as e:
            print(str(e))
            return JsonResponse({'message': e}, safe=False, status=500)

  # Update an article
    if request.method == 'PUT':

        id = request_data['id'] if 'id' in request_data else None
        database_id = request_data['database'] if 'database' in request_data else None
        categoria = request_data['categoria'] if 'categoria' in request_data else None
        codigo = request_data['codigo'] if 'codigo' in request_data else None
        indicexcodigo = request_data['indicexcodigo'] if 'indicexcodigo' in request_data else None
        hipervinculo =  request_data['hipervinculo'] if 'hipervinculo' in request_data else None

        data = {}
        if database_id is not None:
            data['database_id'] = database_id
        if categoria is not None:
            data['categoria'] = categoria
        if codigo is not None:
            data['codigo'] = codigo
        if indicexcodigo is not None:
            data['indicexcodigo'] = indicexcodigo
        if hipervinculo is not None:
            data['hipervinculo'] = hipervinculo

        try:
            response = update_Vinculo(id,data)
            return JsonResponse({'success': response}, safe=False, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': e}, safe=False, status=500)

 # Get storage by location
    if request.method == 'DELETE':
        # id = request.GET.get('id', None)
        # database_id = request_data['database'] if 'database' in request_data else None
        # if id is None:
        #     return JsonResponse({'message': 'id is required'}, safe=False, status=400)

        response = read_Vinculo(request,database, db_name)
        if type(response) == str:
            return JsonResponse({'message': response}, status=400)
        else:
            if len(response) == 0:
                return JsonResponse({'message': 'No records found'}, safe=False, status=200)
            if len(response) == 1:
                id = response[0].id
                database_id = response[0].database_id
                hipervinculo = response[0].hipervinculo
                componentes = hipervinculo.split("/")
                
                # Crea un cliente de S3
                s3 = boto3.client('s3', aws_access_key_id=os.getenv("aws_access_key_id"), aws_secret_access_key='LPsTraFqgII7gxVmwj/m6LSfJ+cIgG51HqMdxcyf', region_name='us-east-1')  # Reemplaza 'us-east-1' con la región correcta
    
                # Nombre del bucket de S3 y clave del objeto de la imagen
                bucket_name = str(componentes[3])
                object_key = f'images/{componentes[5]}/{componentes[6]}/{componentes[7]}'
                try:
                    s3.delete_object(Bucket=bucket_name, Key=object_key)
                    print(f'El objeto {object_key} se ha eliminado con éxito del bucket.')
                except Exception as e:
                    print(f"Error al eliminar el objeto: {str(e)}")

                try:
                    response = delete_Vinculo(id,database_id)
                    if response == 'Deleted successfully':
                        return JsonResponse({'success': 'Deleted successfully'}, safe=False, status=200)
                    else:
                        return JsonResponse({'message': response}, safe=False, status=500)
                except Exception as e:
                    print(e)
                    return JsonResponse({'message': 'Error deleting '}, safe=False, status=500)


@csrf_exempt
def getimage(request):
    try:
        request_data = request._body
        database = request_data['database']

    except Exception as e:
        return JsonResponse({'message': 'Error'}, safe=False, status=500)
    db_name = 'S3'
    if request.method == 'GET':
        print ('GET')

        try:
            # response = read_Vinculo(database_id=database_id,categoria=categoria,codigo=codigo)
            response = read_Vinculo(request,database, db_name)
            if type(response) == str:
                return JsonResponse({'message': response}, status=400)
            else:
                if len(response) == 0:
                    return JsonResponse({'message': 'No records found'}, safe=False, status=200)
                if len(response) == 1:
                    hipervinculo = response[0].hipervinculo
                    componentes = hipervinculo.split("/")
                    
                    # Crea un cliente de S3
                    s3 = boto3.client('s3', aws_access_key_id=os.getenv("aws_access_key_id"), aws_secret_access_key='LPsTraFqgII7gxVmwj/m6LSfJ+cIgG51HqMdxcyf', region_name='us-east-1')  # Reemplaza 'us-east-1' con la región correcta
        
                    # Nombre del bucket de S3 y clave del objeto de la imagen
                    bucket_name = str(componentes[3])
                    object_key = f'images/{componentes[5]}/{componentes[6]}/{componentes[7]}'

                    try:
                        # Descarga la imagen desde S3
                        responseimage = s3.get_object(Bucket=bucket_name, Key=object_key)
                        image_data = responseimage['Body'].read()

                        # Configura la respuesta
                        response2 = HttpResponse(image_data)
                        response2['Content-Type'] = mimetypes.guess_type(f'{componentes[7]}')[0]
                        response2['Content-Disposition'] = f'attachment; filename="{componentes[7]}"'
                        return response2
                    except Exception as e:
                        return HttpResponse('Error al descargar la imagen.', status=500)
                else :
                    return JsonResponse({'message': 'More than one record found'}, safe=False, status=200)  
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'no found'}, safe=False, status=500)


@csrf_exempt
def deletebackground(request):
    try:
        request_data = request._body
        database = request_data['database']

    except Exception as e:
        return JsonResponse({'message': 'Error'}, safe=False, status=500)

    if request.method == 'POST':
                
        file = request.FILES.get('archivo')
        if file:
            uploaded_image =file.read()
            file_extension = file.name.split('.')[-1]
        else:
            print('No file')
            return JsonResponse({'message': 'No file'}, status=400)
        
        try:
            print('Here!')
            # Elimina el fondo de la imagen
            image = rembg.remove(uploaded_image)
            
            
            image_content = image  # Aquí debes tener el contenido de la imagen
            image_extension = file_extension  # Reemplaza con la extensión correcta

            # Configura la respuesta
            response = HttpResponse(image_content)
            response['Content-Type'] = mimetypes.guess_type(f'image.{image_extension}')[0]
            response['Content-Disposition'] = f'attachment; filename="imagen_procesada.{image_extension}"'

            # # Marca la respuesta como segura (HTTPS)
            # response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            return response

        except Exception as e:
            return JsonResponse({'message': 'Error al eliminar el fondo de la imagen'}, status=500)
                
#def maxIdVinculos(request):
#     print ({"request":request._body})
#     try:
#         request_data = request._body
#         database = request_data['database']

#     except Exception as e:
#         return JsonResponse({'message': 'error'}, safe=False, status=500)
#     db_name = 'default'
#     # Get products
#     if request.method == 'GET':
#         print ('GET')

#         database_id = request_data['database'] if 'database' in request_data else None
#         categoria = request.GET.get('categoria', None)
#         codigo = request.GET.get('codigo', None)

#         if database_id is None:
#             return JsonResponse({'message': 'database is required'}, safe=False, status=400)
#         if categoria is None:
#             return JsonResponse({'message': 'categoria is required'}, safe=False, status=400)
#         if codigo is None:
#             return JsonResponse({'message': 'codigo is required'}, safe=False, status=400)

#         try:
#             response = maxid_Vinculo(codigo,categoria,database_id)
#             return JsonResponse({'indice': response}, safe=False, status=200)
#         except Exception as e:
#             print(e)
#             return JsonResponse({'message': 'Error deleting '}, safe=False, status=500)