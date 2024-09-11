# notifications/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('notifications/', view=views.notification_list, name='notification_list'),
    path('notifications/read/<int:notification_id>/', view=views.mark_as_read, name='mark_as_read'),
    path('notifications/read/<int:notification_id>/', view=views.mark_notification_as_read, name='mark_notification_as_read'),

]