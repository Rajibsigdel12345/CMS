from django.urls import path
from .views import UserLoginView, UserSignupView, index , logout_view, UserEditProfileView,remove_profile_pic

app_name = 'user'
urlpatterns = [
  path('login/', UserLoginView.as_view(), name='user_login'),
  path('logout/', logout_view, name='logout'),
  path('signup/', UserSignupView.as_view(), name='user_signup'),
  path('', index, name='index'),
  path('edit/', UserEditProfileView.as_view(), name='user_edit'),
  path('remove/',remove_profile_pic, name='remove_image'),
]