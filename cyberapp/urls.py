from django.urls import path
from . import views

urlpatterns = [
    path('alerts/', views.showAlerts, name="show_alerts"), 
    path('add/', views.add_question, name='add_question'),
    path('viewq/', views.view_questions, name='viewquestion'),
    path('submit_answers/', views.submit_answers, name='submit_answers'),
]
