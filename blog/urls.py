from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<str:month>/<int:day>/<slug:slug>/', views.entry, name='entry'),
    path('blogmark/<int:year>/<str:month>/<int:day>/<slug:slug>/', views.blogmark, name='blogmark'),
    path('<int:year>/', views.year, name='year'),
    path('<int:year>/<str:month>/', views.month, name='month'),
    path('archive/', views.archive, name='archive'),
    path('tag/<slug:slug>/', views.tag, name='tag'),
    path('search/', views.search, name='search'),
    path('feed/', views.AtomFeed(), name='feed'),
]
