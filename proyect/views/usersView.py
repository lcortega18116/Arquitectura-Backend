from django.views.decorators.csrf import csrf_exempt
import os
from django.http.response import JsonResponse
from proyect.functions.usersFunction import *
import json
from django.http import HttpResponse


@csrf_exempt

def usersView(request):
    try:
        print ('PERSON')
        request_data = request.body.decode('utf-8')
    except Exception as e:
        return JsonResponse({'message': e}, safe=False, status=500)
    
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
            data = json.loads(request_data)
            response = createUser(data)
            print(response)
            if response == 'created successfully':
                return JsonResponse({'message': response}, safe=False, status=200)
            return JsonResponse({'message': str(response)}, safe=False, status=400)

        except Exception as e:
            print(str(e))
            return JsonResponse({'message': e}, safe=False, status=500)
        
    if request.method == 'PUT':
        data = json.loads(request_data)
        id = data['id'] if 'id' in data else None
        data.pop('id')


        try:
            response = updateUser(id,data)
            if response == 'updated successfully':
                return JsonResponse({'message': response}, safe=False, status=200)
            return JsonResponse({'message': response}, safe=False, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'message': e}, safe=False, status=500)
        
    if request.method == 'DELETE':
        id = request.GET.get('id', None)
        try:
            response = deleteUser(id)
            if response == 'deleted successfully':
                return JsonResponse({'message': response}, safe=False, status=200)
            return JsonResponse({'message': str(response)}, safe=False, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'message': e}, safe=False, status=500)
