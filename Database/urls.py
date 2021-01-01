"""Database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from restltform.views import (
    returndata,
    storingdata,
    sepcificview,
    deleteview,
    listingusers,
    signup,
    login,
    updatedata,
    logout,
    liked,
    follows,
    profiles,
    comment_post,
    follow_data,
    discover,
    search,
    suggestion,
    suggest_discover,
    returnall,
    chat_dashboard,
    chat,
    profat,
    autocomplete,
    get_comment,
    get_follows_data
    )

urlpatterns = [
    path('',returndata,name='data'),
    path('store',storingdata,name='store'),
    path('<int:my_id>/',sepcificview,name="specific-view"),
    path('<int:my_id>/delete',deleteview,name="delete-view"),
    path('listing/<str:my_username>',listingusers,name="listing"),
    path('signup',signup,name='sign-up'),
    path('login',login,name="login"),
    path('admin/', admin.site.urls),
    path('<int:pk>/update',updatedata,name='update-data'),
    path('logout',logout,name='logout'),
    path('liked/<int:pk>',liked,name='liked'),
    path('follows/<int:pk>',follows,name='follows'),
    path('profiles/<int:pk>',profiles,name="profiles"),
    path('comment/',comment_post,name="comment"),
    path('followsdata',follow_data,name="followsdata"),
    path('new-dis',discover,name="new-dis"),
    path('search/<str:hashtags>',search,name="search"),
    path('suggest_discover/<int:id>',suggest_discover,name="suggest_discover"),
    path('returnall',returnall,name='returnall'),
    path('chat_dashboard',chat_dashboard,name="c_board"),
    path('chatt/<int:id>',chat,name="chatt"),
    path('profat/<str:name>',profat,name='profat'),
    path('autocomplete',autocomplete,name="autocomplete"),
    path('get_comment',get_comment,name="get_comment"),
    path('get_follows_data',get_follows_data,name="get_follows_data")
    
    
]
urlpatterns = urlpatterns+[
    path('chat/', include('chat.urls', namespace='chat')),
]
#urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
