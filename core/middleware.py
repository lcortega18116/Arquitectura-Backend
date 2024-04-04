import json
import jwt
from django.http.response import JsonResponse
from datetime import datetime
import requests


class MiddlewarePerzonalizado:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == 'POST':
                file = request.FILES.get('archivo')
                if file:
                    print (file.name)
            request_data = json.loads(request.body)
        except:
            try:
                request_data = {"data": request.body}
            except:
                request_data = {}

        token = request.headers['Authorization']
        print("The token is: " + token)
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            request_data['database'] = payload['database']
            request_data['id_employee'] = payload['id_employee']
            request_data['warehouse'] = payload['warehouse']
            request_data['id_customer'] = payload['id_customer']
            request_data['role'] = payload['role']

            
            try:
                url = "https://users.copernicowms.com/api/validate"
                headers = {
                    'Authorization': token
                }
                response = requests.request("POST", url, headers=headers)

                if response.status_code == 200:
                    print("VALID TOKEN")
                    request._body = request_data
                    request.db_name = str(request_data['database']) + "_adapter"
                
                else:
                    url = "https://users.copernicowms.com/api/validate/mobile"
                    headers = {
                        'Authorization': token
                    }
                    response = requests.request("POST", url, headers=headers)

                    if response.status_code == 200:
                        print("VALID TOKEN")
                        request._body = request_data
                        request.db_name = str(request_data['database']) + "_adapter"
                    else:
                        print("INVALID TOKEN")
                        return JsonResponse({"error": "Token expired"}, safe=False, status=401)

            except Exception as e:
                print("INVALID TOKEN")
                print(e)
                return JsonResponse({"error": "Token expired"}, safe=False, status=401)
                    

        except jwt.ExpiredSignatureError:
            print("UNEXPECTED EXPIRED SIGNATURE")
            return JsonResponse({"error": "Token expired"}, safe=False, status=401)


        # print("The request data is: " + str(request_data))
        # input("ok")
        # sio.connect('http://localhost:5001')
        # # sio.wait()
        # sio.emit('my_message', {'data': 'my_message'})
        # sio.disconnect()

        return None
