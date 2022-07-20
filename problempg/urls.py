from django.urls import path
from problempg import views

urlpatterns=[
    path('problem/<int:problem_id>/leaderboard',views.usercode,name='leaderboard'),
    path('problem/<int:problem_id>', views.problem_page,name='problem_page'),
]