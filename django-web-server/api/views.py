from django.http import JsonResponse
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime

@api_view(['GET', 'POST'])
def event_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return JsonResponse({"events": serializer.data})
    
    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET'])
def events_by_date(request, year, month, day):
    filter_date = datetime(year, month, day)
    start_of_day = timezone.make_aware(datetime.combine(filter_date, datetime.min.time()))
    end_of_day = timezone.make_aware(datetime.combine(filter_date, datetime.max.time()))
    events = Event.objects.filter(time__range=(start_of_day, end_of_day))

    serializer = EventSerializer(events, many=True)

    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def event_by_id(request, id):
    
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

