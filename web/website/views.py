from django.shortcuts import render

from web.cluster_acc import save_coordinate_to_npy, load_coordinate_stream

# Create your views here.
def index(request):
    x = request.POST['x']
    y = request.POST['y']
    z = request.POST['z']

    save_coordinate_to_npy(x, y, z)
    load_coordinate_stream(x, y, z)

    return render(request, 'index.html', {
            'videos': 'hello',
        })
