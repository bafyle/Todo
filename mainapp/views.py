from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
from .forms import LoginAndRegisterForm

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db.models import Q


@ensure_csrf_cookie
def login_and_register_view(request: HttpRequest):
    if request.method == "POST":
        if request.POST.get("login") == "true":
            form = LoginAndRegisterForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data.get("username"), password=form.cleaned_data.get("password"))
                if user:
                    login(request, user)
                    return JsonResponse({"message": "success"})
            return JsonResponse({"message": "failed"})
        form = LoginAndRegisterForm(request.POST)
        if form.is_valid():
            if get_user_model().objects.filter(username=form.cleaned_data.get("username")).exists():
                return JsonResponse({"message":"username already taken"})
            try:
                validate_password(form.cleaned_data.get("password"))
            except ValidationError as error:
                return JsonResponse({"message":"register-failed", "errors": error.messages}, safe=False)
            new_user = get_user_model()(username=form.cleaned_data.get("username"), password=form.cleaned_data.get("password"))
            new_user.save()
            login(request, new_user)
            return JsonResponse({"message": "success"})
        return JsonResponse({"message":"register-failed", "errors": [error for error in form.errors.values()]})
        
    else:
        if request.user.is_authenticated:
            return redirect("index-view")
        return render(request, 'mainapp/LoginRegister.html')


def logout_view(request):
    logout(request)
    return redirect('login-register')


@login_required(login_url="/login/")
@ensure_csrf_cookie
def index_view(request: HttpRequest):
    return render(request, 'mainapp/index.html', 
        {'object_list': Task.objects.filter(user=request.user).order_by('added_date')}
    )


@api_view(['GET'])
def overview_view(request: HttpRequest):
    api_endpoints = {
        'Overview': 'api/overview/',
        'Create new task': 'api/create/',
        'Delete task': 'api/delete/<id>/',
        'Update task': 'api/update/<id>/',
        'Change completeness of a task':'api/update-completeness/<id>/',
        'Filter tasks': 'api/filter/?order=<asc or desc>&sort=<added date or create date>&filter=<all or active or completed or has_due_date>'
    }
    return Response(api_endpoints)


@login_required(login_url="/login/")
@csrf_protect
@api_view(['GET'])
def filter_view(request: HttpRequest):
    filters = {
        'all': lambda: Task.objects.filter(user=request.user).order_by('added_date'),
        'completed': lambda: Task.objects.filter(user=request.user).order_by('added_date').filter(completed=True),
        'active': lambda: Task.objects.filter(user=request.user).order_by('added_date').filter(completed=False),
        'has_due_date': lambda: Task.objects.filter(user=request.user).order_by('added_date').filter(~Q(due_date=None)),
    }
    filter = request.GET.get('filter')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if filter and sort and order:
        if (query := filters.get(filter)()) != None:
            if order not in ['asc', 'desc']:
                return Response({"message":"bad-sort-type"}, status=403)
            if order == 'desc':
                sort = '-' + sort
            if(query2 := query.order_by(sort)) != None:
                serializer = TaskSerializer(query2, many=True)
                return Response(serializer.data)
    return Response({"message":"bad-filter"}, status=403)


@login_required(login_url="/login/")
@csrf_protect
@api_view(['POST'])
def create_view(request: HttpRequest):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
    return Response(serializer.data)


@login_required(login_url="/login/")
@csrf_protect
@api_view(['DELETE'])
def delete_view(request: HttpRequest, id: int):
    task = Task.objects.filter(id=id, user=request.user)
    deleteted_items, _ = task.delete()
    if deleteted_items > 0:
        return Response(data="Task deleted")
    else:
        return Response(data="Task not deleted", status=404)


@login_required(login_url="/login/")
@csrf_protect
@api_view(['POST'])
def update_view(request: HttpRequest, id: int):
    task = Task.objects.filter(id=id, user=request.user)
    if task.exists():
        task = task.first()
    else:
        return Response({})
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data)
    else:
        return Response("Invalid data")


@login_required(login_url="/login/")
@csrf_protect
@api_view(['POST'])
def update_complete_view(request: HttpRequest, id: int):
    task = Task.objects.filter(id=id, user=request.user)
    if task.exists():
        task = task.first()
    else:
        return Response({})
    task.completed = not task.completed
    task.save()
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)