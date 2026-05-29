
import requests
from .models import SearchHistory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

API_KEY = '47e9128e39140f9e61cdb66c6dcbe4b0'


def home(request):
    weather_data = None

    if request.method == 'POST':
        city = request.POST.get('city')

        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
            }

            # 💾 сохраняем только если пользователь вошёл
            if request.user.is_authenticated:
                SearchHistory.objects.create(
                    user=request.user,
                    city=city,
                    temperature=data['main']['temp'],
                    description=data['weather'][0]['description'],
                    humidity=data['main']['humidity']
                )

    return render(request, 'weather/home.html', {'weather': weather_data})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'weather/register.html', {'form': form})



@login_required
def history(request):
    history = SearchHistory.objects.filter(user=request.user).order_by('-search_date')
    return render(request, 'weather/history.html', {'history': history})