from django.shortcuts import render
from .image_processing import get_frame
from django.http import JsonResponse

def check_new_frame(request):
    get_frame()
    return JsonResponse({"status": "Image processed"})