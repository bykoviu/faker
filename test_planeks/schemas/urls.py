
from django.urls import path
from . import views
from .views import LoginUser, logout_user, RegisterUser

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('schemas/', views.schemas, name='schemas'),
    path('create-schema/', views.create_schema, name='new-schema'),
    path('schema/<int:id>', views.single_schema, name='single-schema'),
    path('column/<int:pk>/update', views.UpdateColumnView.as_view(), name='update-column'),
    path('column/<int:pk>/delete', views.DeleteColumnView.as_view(), name='delete-column'),
    path('schema/<int:id>/create-csv', views.create_csv, name='create-csv'),


]
