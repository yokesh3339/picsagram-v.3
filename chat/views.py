from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restltform.models import follow
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
# Create your views here.
def index(request):
    return render(request, 'chat/index.html')
@login_required
def room(request, room_name):
    if request.user.username>room_name:
        main_name=request.user.username+room_name
    else:
        main_name=room_name+request.user.username
    rec=get_object_or_404(User,username=room_name)
    followings=request.user.profile_user.followers_users.all().union(request.user.profile_user.following_users.all())
    return render(request, 'chat/room.html', {
        'room_name': main_name,
        'username':request.user.username,
        'sender':request.user.profile_user,
        'reciver':rec.profile_user,
        'followings':followings
    })