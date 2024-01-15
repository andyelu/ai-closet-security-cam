from django.urls import path
from . import views

urlpatterns = [
    path('event', views.event_list),
    path('event/<int:year>/<int:month>/<int:day>/', views.events_by_date),
    path('event/<int:id>', views.event_by_id)
]