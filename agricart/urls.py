from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('cropguide',views.cropguide,name="cropguide"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('result',views.result,name="result"),

    path('disease',views.disease,name="disease"),
    path('disease_result',views.disease_result,name="disease_result"),

    path('fertilizer',views.fertilizer,name="fertilizer"),
    path('fertilizer_result',views.fertilizer_result,name="fertilizer_result"),

    path("chat/", views.chat, name="chat"),
    
]

