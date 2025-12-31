import requests 
from django.shortcuts import render # type: ignore

from weather import settings
from .models import SearchHistory
api_key = settings.OPENWEATHER_API_KEY

# Create your views here.
def index(request):
    weather=None
    error=None
    recent_searches=SearchHistory.objects.order_by('searched_at')[:5]

    if request.method=="POST":
        city=request.POST.get('city','').strip()
        if city:
            url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={"a0b4bbca5c36b0832d2e5a97ba8aec0c"}&units=metric"
            resp=requests.get(url)
            data=resp.json()

            if resp.status_code==200:
                weather= {
                    'city': f"{data['name']}, {data['sys']['country']}",
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                }
                SearchHistory.objects.create(
                    city_name=data['name'],
                    temperature=data['main']['temp'],
                    humidity=data['main']['humidity'],
                    pressure=data['main']['pressure'],
                    description=data['weather'][0]['description'].title()
                )
                recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]
            else:
                error = data.get("message", "Could not fetch weather")
        else:
            error = "Enter a city name."

    return render(request, "main/index.html", {
        'weather': weather,
        'error': error,
        'recent_searches': recent_searches
    })

