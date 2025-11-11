from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

# Create your views here.
@login_required 
def task_list(request):
    """Displays the user's task list and handles task creation."""
    tasks = Task.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user 
            new_task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
        
    context = {'tasks': tasks, 'form': form}
    return render(request, 'to_do.html', context)

@login_required
def complete_task(request, pk):
    """Toggles the 'completed' status of a task."""
    task = get_object_or_404(Task, pk=pk, user=request.user) 
    
    # Toggle the status
    task.completed = not task.completed
    task.save()
    
    # Send user back to the main list
    return redirect('task_list')

@login_required
def delete_task(request, pk):
    """Deletes a task."""
    # Ensure the task exists AND belongs to the user
    task = get_object_or_404(Task, pk=pk, user=request.user) 
    task.delete()
    
    # Send user back to the main list
    return redirect('task_list')