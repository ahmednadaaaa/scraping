from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_page, name='job_search_page'),
    path('jobs/<str:search_job>/<int:page_num>/', views.scrape_jobs, name='scrape_jobs_search'),
    
]