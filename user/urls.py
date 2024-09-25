from django.urls import path
from .views import UserLoginView, UserSignupView, index , logout_view

app_name = 'user'
urlpatterns = [
  path('login/', UserLoginView.as_view(), name='user_login'),
  path('logout/', logout_view, name='logout'),
  path('signup/', UserSignupView.as_view(), name='user_signup'),
  path('', index, name='index')
]