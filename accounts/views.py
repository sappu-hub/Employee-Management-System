from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    return render(request, 'accounts/login.html')

from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        else:
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'Registration successful'}, status=200)
    return render(request, 'accounts/register.html')

from django.contrib.auth import update_session_auth_hash

def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if not request.user.check_password(old_password):
            return JsonResponse({'error': 'Incorrect old password'}, status=400)
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Keep user logged in
        return JsonResponse({'message': 'Password changed successfully'}, status=200)
    return render(request, 'accounts/change_password.html')

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')

        # Update the user's profile
        try:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            return JsonResponse({'message': 'Profile updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Error updating profile: {str(e)}'}, status=500)

    # Render the profile page
    return render(request, 'accounts/profile.html', {'user': request.user})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import DynamicForm
import json

@csrf_exempt
def create_dynamic_form_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Get JSON data from the request
            form_name = data.get('name')
            configuration = data.get('configuration', [])

            # Save the form configuration
            dynamic_form = DynamicForm.objects.create(name=form_name, configuration=configuration)
            return JsonResponse({'message': 'Form created successfully!', 'form_id': dynamic_form.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Error creating form: {str(e)}'}, status=500)

    return render(request, 'accounts/create_dynamic_form.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import DynamicForm

@csrf_exempt
def save_dynamic_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            configuration = data.get('configuration')

            # Save form to database
            form = DynamicForm.objects.create(name=name, configuration=configuration)
            return JsonResponse({'success': True, 'form_id': form.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

from django.shortcuts import render
from .models import DynamicForm

def list_saved_forms(request):
    forms = DynamicForm.objects.all()
    return render(request, 'list_saved_forms.html', {'forms': forms})

def use_form(request, form_id):
    form = DynamicForm.objects.get(id=form_id)
    return render(request, 'use_form.html', {'form': form})

