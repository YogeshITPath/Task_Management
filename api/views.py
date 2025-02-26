# Django and DRF imports
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# imports Task
from tasks.models import Task
from .serializers import TaskSerializer


class RegisterAndGenerateTokenView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        password_confirmation = request.data.get('password_confirmation')

        if not username or not password or not password_confirmation:
            return Response(
                {"error": "Username, password, and password confirmation are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != password_confirmation:
            return Response(
                {"error": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "User with this username already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            username=username,
            password=make_password(password)
        )

        return Response(
            {
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED
        )


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        try:
            task = self.get_object()
            task.is_completed = not task.is_completed
            task.save()
            return Response(
                {'status': 'Task status toggled', 'is_completed': task.is_completed},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Task created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Failed to create task", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Task updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Failed to update task", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Task deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class ToggleTaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.is_completed = not task.is_completed
            task.save()
            return Response(
                {"status": "success", "message": "Task status toggled successfully", "is_completed": task.is_completed},
                status=status.HTTP_200_OK
            )
        except Task.DoesNotExist:
            return Response(
                {"status": "error", "message": "Task not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
