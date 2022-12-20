from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('create_event', views.create_event, name="create_event"),
    # path('liked/<int:event_id>/', views.liked, name="liked"),
    # path("unliked/<int:event_id>/", views.unliked, name="unliked"),
    path("liked_events/", views.liked_events, name="liked_events"),
    path("clicked/", views.clicked, name="clicked"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
