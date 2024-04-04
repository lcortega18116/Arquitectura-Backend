from django.views.decorators.csrf import csrf_exempt
import os
from django.http.response import JsonResponse
from proyect.functions.usersFunction import *
import json
from django.http import HttpResponse
from dotenv import load_dotenv

load_dotenv()

@csrf_exempt

def usersView(request):
    
    if request.method == 'GET':
        print ('GET')

        try:
            response = readUser(request)
            if type(response) == str:
                return JsonResponse({'message': response}, status=204)
            else:
                if len(response) == 0:
                    return JsonResponse({'message': 'No hay usuario registrado'}, safe=False, status=204) 
                response_json = list(response.values())
                return JsonResponse(response_json, safe=False, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': e}, safe=False, status=500)
    if request.method == 'POST':
        try:
            request_data = request._body    
        except Exception as e:
            return JsonResponse({'message': 'Error'}, safe=False, status=500)
        try:
            response = createUser(request_data)
            if response == 'created successfully':
                return JsonResponse({'message': response}, safe=False, status=200)

        except Exception as e:
            print(str(e))
            return JsonResponse({'message': e}, safe=False, status=500)
        
    if request.method == 'PUT':
        try:
            request_data = request._body    
        except Exception as e:
            return JsonResponse({'message': 'Error'}, safe=False, status=500)
        
        id = request_data['id'] if 'id' in request_data else None
        data = request_data.pop('id')
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
            response = updateUser(id,data)
            if response == 'updated successfully':
                return JsonResponse({'message': response}, safe=False, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': e}, safe=False, status=500)
        
    if request.method == 'DELETE':
        id = request.GET.get('id', None)
        try:
            response = deleteUser(id)
            if response == 'deleted successfully':
                return JsonResponse({'message': response}, safe=False, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': e}, safe=False, status=500)
