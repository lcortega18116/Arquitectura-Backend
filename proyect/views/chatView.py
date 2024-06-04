from django.views.decorators.csrf import csrf_exempt
import os
from django.http.response import JsonResponse
from proyect.functions.chatFunction import *
import json
from django.http import HttpResponse


@csrf_exempt

def chatView(request):
    try:
        print ('Chat')
        request_data = request.body.decode('utf-8')
    except Exception as e:
        return JsonResponse({'message': e}, safe=False, status=500)
    
    if request.method == 'GET':
        print ('GET')

        try: 
            response = readResumen(request)
            message = request.GET.get('message', '')
            if type(response) == str:
                return JsonResponse({'message': response}, status=204)
            else:
                if len(response) == 0:
                    return JsonResponse({'message': 'No hay asistencias registradas'}, safe=False, status=204) 
                else:
                    result = send_chat_request(message, str(response))
                    assistant_response = result["choices"][0]["message"]["content"]
                    print(assistant_response)
                    return JsonResponse({'message': str(assistant_response)}, safe=False, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': e}, safe=False, status=500)
    