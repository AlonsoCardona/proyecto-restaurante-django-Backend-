from django.urls import path
from . import views

app_name = 'platillos'

urlpatterns = [    
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/add/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/edit/', views.CategoriaUpdateView.as_view(), name='categoria_edit'),
    path('categorias/<int:pk>/delete/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
    path('platillos/', views.PlatilloListView.as_view(), name='platillos_list'),
    path('platillos/add/', views.PlatilloCreateView.as_view(), name='platillos_create'),
    path('platillos/<int:pk>/edit/', views.PlatilloUpdateView.as_view(), name='platillos_edit'),
    path('platillos/<int:pk>/delete/', views.PlatilloDeleteView.as_view(), name='platillos_delete'),
]