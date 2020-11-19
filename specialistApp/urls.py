from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.RandomSelectView.as_view()),
    path('print/', views.PrintView.as_view()),
    path('upload/', views.UploadView.as_view()),
    path('statistic/', views.StatisticView.as_view()),
    path('statistic/<str:category>', views.StatisticCategoryView.as_view()),
    path('statistic/check/', views.CheckView.as_view()),
    path('statistic/refreshage/', views.refreshAgeView.as_view()),
]
