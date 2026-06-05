from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
   path('',views.index,name="index"),
   path('aboutus',views.aboutus, name="aboutus"),

   #Account Registration
   path('registeracc',views.registeracc,name="registeracc"),
   #login 
   path('loginacc',views.loginacc,name="loginacc"),
   #bookevent
   path('bookevent',views.bookevent,name="bookevent"),
   #after login page 
   path('index2/',views.index2,name="index2"),
   path('index2/aboutus2',views.aboutus2, name="aboutus2"),
   path('index2/bookevent2',views.bookevent2,name="bookevent2"),
   path('index2/registerevent', views.registerevent, name='registerevent'),

   #user dashboard 
   path('index2/userdashboard/',views.userdashboard,name="userdashboard"),
   path('index2/userdashboard/userdashboard_update/<int:userID>/', views.userdashboard_update, name="userdashboard_update"),
   
   #user review
   path('index2/display_review/',views.display_review, name="display_review"),
   path('index2/display_review/review',views.review,name="review"),
   path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
   path('index2/display_review/review/edit/<int:review_id>/', views.edit_review, name='edit_review'),

   #user log out 
   path('index2/sign-out/', views.sign_out, name='sign_out'),


]


urlpatterns += staticfiles_urlpatterns()
