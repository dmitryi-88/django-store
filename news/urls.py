from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.NewsListView.as_view(), name="news_list"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("create/", views.NewsCreateView.as_view(), name="news_create"),
    path("<int:pk>/edit/", views.NewsUpdateView.as_view(), name="news_update"),
    path("<int:pk>/delete/", views.NewsDeleteView.as_view(), name="news_delete"),
    path("<int:pk>/", views.NewsDetailView.as_view(), name="news_detail"),
]
