import io
import json
import os
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
import plotly.graph_objs as go

from core import settings
from .models import TestResult, UserProfile

# Create your views here.
def test(request):
    return render(request,'index.html')


def get_random_text_prompt(request):
    text_type = request.GET.get('textType')
    file_mapping = {
        '1': 'words.txt',
        '2': 'punctuation.txt',
        '3': 'topRow.txt',
        '4': 'homeRow.txt',
        '5': 'bottomRow.txt'
    }
    
    file_name = file_mapping.get(text_type)
    if not file_name:
        return HttpResponse('Invalid textType', status=400)
    
    file_path = os.path.join(settings.BASE_DIR, 'RapidType', 'static', 'textFiles', file_name)
    
    with open(file_path, 'r') as file:
        words = file.read().split()


    random_text = random.sample(words, min(220,len(words)))

    random_text = ' '.join(random_text)

    return HttpResponse(random_text)





def generate_graph(request):
    if request.method == 'POST':
        try:
       
            data = json.loads(request.body.decode('utf-8'))
            wpm_data = data.get('wpm_data', [])
            if not wpm_data:
                raise ValueError('No wpm_data provided')
            
 
            step_size = 3
            x_axis_points = [i * step_size for i in range(1, len(wpm_data) + 1)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_axis_points, y=wpm_data, mode='lines', line=dict(color='#e2bb39')))
            fig.update_layout(
                title='Words Per Minute (WPM)',
                xaxis=dict(title='Time Interval', color='#e2bb39', showgrid=True, gridcolor='#555', gridwidth=0.5),
                yaxis=dict(title='WPM', color='#e2bb39', showgrid=True, gridcolor='#555', gridwidth=0.5),
                plot_bgcolor='#22252d',
                paper_bgcolor='#22252d',
                font=dict(color='#e2bb39', size=12),
                margin=dict(l=40, r=40, t=60, b=40),
            )
            
     
            image_stream = io.BytesIO()
            fig.write_image(image_stream, format='png')
            image_stream.seek(0)
            
      
            response = HttpResponse(image_stream.read(), content_type='image/png')
            image_stream.close()
            return response
        except Exception as e:
            return HttpResponseBadRequest('Invalid request')


def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if email or username already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup') 

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup') 

        user = User.objects.create_user(email=email, username=username, password=password)
        UserProfile.objects.create(user=user)
        messages.success(request, "Account created successfully. You can now login.")
        return redirect('signup')  

    return render(request, 'signup.html')

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username')
            return redirect('loginpage')
        
        user = authenticate(username=username,password=password)
        
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('loginpage')
        else:
            login(request, user)
            return redirect('test')
    return render(request,'login.html')

@login_required
def logoutpage(request):
    logout(request)
    return redirect('/')


def save_test_result(request):
    if request.method == 'POST':
        try:
        
            data = json.loads(request.body.decode('utf-8'))
            
         
            wpm = data.get('wpm')
            accuracy = data.get('accuracy')
            test_time = data.get('testTime')
            text_type = data.get('textType')
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            test_result = TestResult.objects.create(
                user_profile=user_profile,
                wpm=wpm,
                accuracy=accuracy,
                test_time=test_time,
                text_type=text_type
            )
            
            return JsonResponse({'message': 'Test result saved successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def leaderboard(request):
    top_performers = TestResult.objects.filter(accuracy__gte=85).order_by('-wpm')[:25]
    
  
    return render(request, 'leaderboard.html', {'top_performers': top_performers})


@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    if user_profile:
        test_results = TestResult.objects.filter(user_profile=user_profile).order_by('-test_date')
    else:
        test_results = []

    return render(request, 'profile.html', {'test_results': test_results})  