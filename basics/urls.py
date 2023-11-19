from django.urls import path
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<id>/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('newbusiness/', views.newbusiness, name='newbusiness'),
    path('business/<id>', views.business, name='business'),
    path('search/', views.search, name='search'),
    path('searchb/', views.searchb, name='searchb'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
