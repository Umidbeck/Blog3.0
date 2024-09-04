from django.urls import path
from .views import HomePageView, AboutPageView, ContactPageView, DetailPageView, BlogPageView, SearchResultsView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('post/<int:pk>/', DetailPageView.as_view(), name='post_detail'),
    path('blog/', BlogPageView.as_view(), name='blog'),
    path('search/', SearchResultsView.as_view(), name='search'),
]