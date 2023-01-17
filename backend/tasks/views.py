from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse

from .serializers import TaskSerializer

from .models import Task

@csrf_exempt
def tasks(request):
    if (request.method == 'GET'):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

        return JsonResponse(serializer.data, safe=False)

    elif (request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        serializer.save()
        return JsonResponse(serializer.data, status=201)

@csrf_exempt
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if (request.method == 'PUT'):
        data = JSONParser.parse(request)
        serializer = TaskSerializer(task, data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        serializer.save()
        return JsonResponse(serializer.data, status=201)
    
    elif (request.method == 'DELETE'):
        task.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=403)
