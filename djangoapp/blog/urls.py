from django.urls import path
from .views import index, post, page, created_by, category

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('post/<slug:slug>/', post, name='post'),
    path('page/<slug:slug>/', page, name='page'),
    path('created_by/<int:author_id>/', created_by, name='created_by'),
    path('category/<slug:slug>/', category, name='category'),

]
