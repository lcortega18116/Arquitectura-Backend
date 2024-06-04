from django.http import JsonResponse
from ..models import Person, Class, Grade ,Presence
from django.db.models import Count
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


def readResumen(request):
    # Obtener parámetros de la solicitud
    teacher_id = request.GET.get('teacher_id', '')
    class_code = request.GET.get('class_code', '')

    # Obtener el queryset filtrado de presencias
    presence_queryset = Presence.objects.filter(teacher_id=teacher_id, class_code=class_code)

    # Agrupar por student_id, contar la cantidad de repeticiones y obtener el class_code
    grouped_data = presence_queryset.values('student_id', 'class_code').annotate(count=Count('student_id'))

    # Convertir el queryset a una lista de diccionarios
    grouped_data_list = list(grouped_data)

    # Agregar el nombre y apellido del estudiante a cada elemento del diccionario
    for item in grouped_data_list:
        student_id = item['student_id']
        student = Person.objects.get(id=student_id)
        item['student_name'] = student.firstname
        item['student_lastname'] = student.lastname
        item['assists'] = item['count']
        item.pop('class_code', None)
        item.pop('student_id', None)
        item.pop('count', None)

        # Obtener las calificaciones del estudiante para la clase específica
        grades = Grade.objects.filter(student_id=student_id, class_code=class_code)
        
        # Inicializar lista para almacenar las calificaciones
        grades_list = []
        
        # Iterar sobre las calificaciones del estudiante
        for grade in grades:
            grade_data = {
                'grade': grade.grade,
                'percent': str(grade.percent) +' %'
            }
            grades_list.append(grade_data)

        # Agregar la lista de calificaciones al diccionario
        item['grades'] = grades_list

    # Obtener el nombre de la clase
    class_name = Class.objects.get(code=class_code).name

    # Retornar la lista de diccionarios junto con el nombre de la clase
    return {'class_name': class_name,'data': grouped_data_list}
    

def send_chat_request(message,data):
    url = os.getenv('url')
    token = os.getenv('token')
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "assistant", 
                "content": data
            },
            {
                "role": "assistant", 
                "content": message
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}", "details": response.text}
