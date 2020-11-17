from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.RandomSelectView.as_view()),
    path('print/',views.PrintView.as_view()),
    path('upload/',views.UploadView.as_view())
]
