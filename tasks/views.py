from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control
from .models import Task
from .forms import TaskForm




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        # Create session data
        self.request.session['username'] = user.username
        self.request.session['user_id'] = user.id
        messages.success(self.request, f'Welcome, {user.username}!')
        return super().form_valid(form)

# Prevent caching for logged-in pages
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tasks/task_list.html', {'page_obj': page_obj, 'username': request.session.get('username')})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('task_list')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def toggle_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.status = not task.status #flipping condition True then Masked as completed & False means Mark as Pending.
    task.save()
    messages.success(request, 'Task status updated!')
    return redirect('task_list')
