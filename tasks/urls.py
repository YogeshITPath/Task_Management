from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomLoginView

urlpatterns = [
    # User Registration and Authentication
    path('', views.register, name='register'),  # User registration
    path('login/', CustomLoginView.as_view(), name='login'),  # Custom login view

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout redirects to login

    # Task Management
    path('tasks/', views.task_list, name='task_list'),  # List of tasks
    path('tasks/add/', views.add_task, name='add_task'),  # Add a new task
    path('tasks/edit/<int:id>/', views.edit_task, name='edit_task'),  # Edit a specific task
    path('tasks/delete/<int:id>/', views.delete_task, name='delete_task'),  # Delete a specific task
    path('tasks/toggle/<int:id>/', views.toggle_task, name='toggle_task'),  # Toggle task completion status
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
