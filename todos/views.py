# todos/views.py
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import Todo
from .serializers import TodoSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "is_priority"]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    @method_decorator(csrf_protect)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @method_decorator(csrf_protect)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @method_decorator(csrf_protect)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class TodoPrioritiesView(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user, is_priority=True)


class TodoStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Todo.objects.filter(user=request.user)
        total_todos = queryset.count()
        completed_todos = queryset.filter(status="done").count()
        return Response(
            {
                "total_todos": total_todos,
                "completed_todos": completed_todos,
                "completion_rate": (
                    f"{(completed_todos / total_todos * 100):.2f}%"
                    if total_todos
                    else "0%"
                ),
            }
        )
