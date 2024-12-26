from django.shortcuts import render, redirect, get_object_or_404
from .models import Whiteboard
from .forms import WhiteboardForm
from django.contrib.auth.decorators import login_required

def whiteboard(request, board_id):
    whiteboard = Whiteboard.objects.get(id=board_id)
    return render(request, 'collaborative_tools/whiteboard.html', {'whiteboard': whiteboard})

# View to list all whiteboards
@login_required
def list_whiteboards(request):
    whiteboards = Whiteboard.objects.all()
    return render(request, 'collaborative_tools/whiteboard_list.html', {'whiteboards': whiteboards})

# View to create a new whiteboard
@login_required
def create_whiteboard(request):
    if request.method == 'POST':
        form = WhiteboardForm(request.POST)
        if form.is_valid():
            whiteboard = form.save(commit=False)
            whiteboard.created_by = request.user
            whiteboard.save()
            return redirect('list_whiteboards')
    else:
        form = WhiteboardForm()
    return render(request, 'collaborative_tools/create_whiteboard.html', {'form': form})

