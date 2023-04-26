"""taskapplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name="signup"),
    path('login/',views.SignInView.as_view(),name="signin"),
    path('logout/',views.signout_view,name="signout"),

    path('index/',views.IndexView.as_view(),name="index"),
    path('todos/add/',views.TaskCreateView.as_view(),name="add"),
    path('todos/all/',views.TaskListView.as_view(),name="list"),
    path("todos/<int:pk>/detail/",views.TaskDetailView.as_view(),name="task-detail"),
    path("todos/<int:pk>/edit/",views.TaskUpdateView.as_view(),name="task-edit"),
    path("todos/<int:pk>/remove/",views.taskdelete_View,name="task-delete"),
    path("password/change/",views.PasswordResetView.as_view(),name="password-reset")
]

