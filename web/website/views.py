from django.shortcuts import render

# Create your views here.
def index(request):
    x = request.POST['x']
    y = request.POST['y']
    z = request.POST['z']

    return render(request, 'index.html', {
            'videos': 'hello',
        })
