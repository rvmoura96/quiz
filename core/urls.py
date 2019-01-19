from django.contrib import admin
from django.urls import path, include

import core.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('detalhes-questionario/<int:id>', views.detalhes_questionario, name='detalhes-questionario')
]
