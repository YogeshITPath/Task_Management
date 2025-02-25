from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Task
from .serializers import TaskSerializer


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users only

    def get_queryset(self):
        # Return tasks belonging to the logged-in user
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the task with the logged-in user
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        # Override the post method to provide custom responses
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(
                {"message": "Task created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Failed to create task", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users only

    def get_queryset(self):
        # Return tasks belonging to the logged-in user
        return Task.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        # Override the put method to provide custom responses
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Task updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Failed to update task", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, *args, **kwargs):
        # Override the delete method to provide custom responses
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
