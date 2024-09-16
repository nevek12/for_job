from django.shortcuts import render

# Create your views here.

def index(request):
    data = {
        'title': 'Главная страница',
        'values': ['Some', 'Hello', 123],
        'obj': {
            'car': 'BMW',
            'age': 18,
            'hobby': 'Football'
        }
    }
    return render(request, 'vladosos/index.html', data)

def about(request):
    return render(request, 'vladosos/about.html')