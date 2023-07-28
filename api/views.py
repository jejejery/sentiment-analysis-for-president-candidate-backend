# api/views.py
import json
from algo.parser import *
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def receive_json(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            
            parser = Parser(Parser.clear_arr(json_data))
            arr_of_json = parser.tuples

            # Mengonversi arr_of_json menjadi bentuk string JSON
                

            # Kirimkan sebagai JSON response
            return JsonResponse(arr_of_json, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    return JsonResponse({'message': 'Bad Request'}, status=400)


