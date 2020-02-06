from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo import views

router = DefaultRouter()
router.register(r'groupOfTasks', views.GroupOfTasksViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'folder', views.FolderViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]