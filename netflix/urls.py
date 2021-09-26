
from django.conf.urls import url
from netflix.views import home, index,login,signup,logout,video_play
from django.urls import path




urlpatterns = [
    path('index/',index,name='index'),
    path('login/',login,name='login'),
    path('signup/',signup,name='signup'),
    path('home/', home, name='home'),
    path('logout/',logout,name='logout'),
    path('home/<slug>/',video_play,name='unique_slug')
]