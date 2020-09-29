from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('aarelays.basic_access')
def index(request):
        
    context = {
        'text': 'Hello, World!'
    }    
    return render(request, 'aarelays/index.html', context)
