# todos/urls.py
from django.urls import path
from .views import (
    TodoListCreateView,
    TodoRetrieveUpdateDestroyView,
    TodoPrioritiesView,
    TodoStatsView,
)

urlpatterns = [
    path("", TodoListCreateView.as_view(), name="todo-list-create"),
    path("<uuid:pk>/", TodoRetrieveUpdateDestroyView.as_view(), name="todo-detail"),
    path("priorities/", TodoPrioritiesView.as_view(), name="todo-priorities"),
    path("stats/", TodoStatsView.as_view(), name="todo-stats"),
]
