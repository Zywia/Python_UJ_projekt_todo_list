from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'group', views.GroupOfTasksViewSet)
router.register(r'todo', views.TaskViewSet)
router.register(r'folder', views.FolderViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]