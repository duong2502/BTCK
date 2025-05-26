from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')

router.register('companies', views.CompanyViewSet, basename='company')

router.register('jobs', views.JobViewSet, basename='job')
router.register('users', views.UserViewSet, basename='user')
router.register('comments', views.CommentViewSet, basename='comment')
#
# router.register('posts', views.PostViewSet, basename='post')
#
urlpatterns = [
    path('', include(router.urls)),

]