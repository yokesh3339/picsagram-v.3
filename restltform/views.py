from django.shortcuts import render,HttpResponseRedirect,reverse
from .forms import PeopleForm,UserCreate,loginform,UserProfile
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import People,follow,comments,hashtag
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import json
from random import shuffle
import random
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.contrib.auth.decorators import login_required
from chat.views import room
import cv2
import os
import numpy as np
import pandas as pd
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
#from .apps import machine_model
# Create your views here.
def returndata(request):
    obj=People.objects.all()
    obj=obj.order_by('?')
    global obj_for_ajax_discover
    obj_for_ajax_discover=list(obj)
    if request.user.is_authenticated:
        objs={'obj':obj_for_ajax_discover[:5],'loginuser':str(request.user)}
    else:
        objs={'obj':obj_for_ajax_discover[:5],'loginuser':str(request.user)}
    obj_for_ajax_discover=obj_for_ajax_discover[5:]
    return render(request,'index.html',objs)
@login_required
def follow_data(request):
    """     people_obj=People.objects.all().order_by("-pk")
    obj_fol=follow.objects.all()
    cmt_user=comments.objects.all()
    obj=[]
    f=follow.objects.get(user=request.user)
    for i in people_obj: 
        if i.users in f.followed_users():
            obj.append(i) """
    obj=People.objects.none()
    following_user_all=request.user.profile_user.following_users.all()
    global obj_for_ajax
    for usr in following_user_all:
        obj=obj.union(usr.post_user.all())
    obj=obj.union(request.user.post_user.all())
    obj_for_ajax=list(obj.order_by("-id"))
    objs={'obj':obj_for_ajax[:5],'loginuser':str(request.user)}
    obj_for_ajax=obj_for_ajax[5:]
    return render(request,'index.html',objs)
def get_follows_data(request):
    path=request.GET["path"]
    if path=="followsdata":
        global obj_for_ajax
        objs={'obj':obj_for_ajax[:5]}
        obj_for_ajax=obj_for_ajax[5:]
        return render(request,'add_post.html',objs)
    elif path=="":
        global obj_for_ajax_discover
        objs={'obj':obj_for_ajax_discover[:2]}
        obj_for_ajax_discover=obj_for_ajax_discover[2:]
        return render(request,'add_post.html',objs)
    elif path=="new-dis":
        global obj_for_ajax_discover_sug
        objs={'obj':obj_for_ajax_discover_sug[:5]}
        obj_for_ajax_discover_sug=obj_for_ajax_discover_sug[5:]
        return render(request,'new_dis_ajax.html',objs)
    elif path=="suggest_discover":
        global ajax_suggest_discover
        objs={'obj':ajax_suggest_discover[:3]}
        ajax_suggest_discover=ajax_suggest_discover[3:]
        print(123)
        return render(request,'add_post.html',objs)
        
    return render(request,'add_post.html',{})
@login_required
def storingdata(request):
    username=str(request.user)
    obs={'username':username}
    form=PeopleForm(initial=obs)
    f=follow.objects.get(user=request.user)
    if request.method=='POST':
        form=PeopleForm(request.POST,request.FILES)
        if form.is_valid():
            form=form.cleaned_data
            form['users']=request.user
            form['follow']=f
            form['description']=form['description'].lower()
            p=People.objects.create(**form)
            tags=hashtagfinder(form['description'])
            for tag in tags:
                h=hashtag.objects.filter(tag=tag)
                if not h.exists():
                    h=hashtag.objects.create(tag=tag)
                    h.post.add(p)
                else:
                    h[0].post.add(p)
            #generate hashtag model
            autorun()
            return HttpResponseRedirect(reverse('data'))
    content={'forms':form}
    return render(request,'datacollect.html',content)
def get_relation(tags):
    df2=pd.read_excel(os.path.join(BASE_DIR, ".", "df2.xlsx"),engine='openpyxl',index_col=0)
    try:
        dframe=df2.loc[tags].sort_values(ascending=False)
        dframe=dframe.loc[dframe!=0]
        return list(dframe.index)
    except Exception as e:
        return None
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def generate_hashtag(request):
    if request.method=='POST':
        #image classification
        img=request.FILES['profile']
        fs=FileSystemStorage()
        file=fs.save(img.name,img)
        fileurl=fs.url(file)
        im=cv2.imread("."+fileurl)
        im=im/255
        os.remove("."+fileurl)
        im=cv2.resize(im,(32,32))
        #plt.imshow(im)
        im=im.reshape(1,32,32,3)
        classes=["airplane","automobiles","bird","cat","deer","dog","frog","horse","ship","truck"]
        m=tf.keras.models.load_model("models/image.h5")
        print(classes[np.argmax(m.predict(im))])
        tagss=classes[np.argmax(m.predict(im))]
        lis=get_relation(tagss)
        if lis:
            lis[0]="#"+lis[0]
            l=" #".join(lis)
        else:
            l="#"+tagss
        return HttpResponse(l)
def autorun():
    df=pd.DataFrame.from_records(hashtag.objects.all().values_list('pk','tag','post','suggest_tag'))
    df[3]=df[3].astype('Int64')
    #df.rename(columns={'0':'tag_id','1':'tag','2':'post_id'},inplace=True)
    df.rename(columns={0:'tag_id',1:'tag',2:'post_id',3:'suggest_user'},inplace=True)
    df=df.fillna(0)
    #id=df.loc[df.tag=='ipl']
    df=df.sort_values('post_id')
    df=df.drop(['suggest_user'],axis=1)
    df.drop_duplicates(inplace=True)
    arr=df.tag.unique()
    df2=pd.DataFrame(index=arr,columns=arr)
    df2=df2.fillna(0)
    i=j=k=0
    arr=df.tag.unique()
    df2=pd.DataFrame(index=arr,columns=arr)
    df2=df2.fillna(0)
    for i in df.post_id.unique():
        for j in df.loc[df.post_id==i].tag:
            for k in df.loc[df.post_id==i].tag:
                df2[j][k]+=1
    df.loc[df.post_id==20].tag
    df2.to_excel("df2.xlsx")
def sepcificview(request,my_id):
    obj=get_object_or_404(People,id=my_id)
    obj=[obj]
    obj_fol=follow.objects.all()
    cmt_user=comments.objects.all()
    if request.user.is_authenticated:
        suggestion(request,my_id)
        contents={'obj':obj,'cmt_user':cmt_user}
    else:
        contents={'obj':obj}
    return render(request,'index.html',contents)
@login_required
def deleteview(request,my_id):
    obj=get_object_or_404(People,id=my_id)
    if request.method=="POST":
        obj.delete()
        return redirect('../')
    return render(request,"delete_code.html",{'obj':obj})
def listingusers(request,my_username):
    obj=People.objects.filter(username=my_username)
    obj_fol=follow.objects.all()
    if request.user.is_authenticated:
        contents={'obj':obj}
    else:
        contents={'obj':obj}
    return render(request,'index.html',contents)
def signup(request):
    form=UserCreate()
    form1=UserProfile()
    if request.method=='POST':
        form=UserCreate(request.POST)
        form1=UserProfile(request.POST,request.FILES)
        if form.is_valid() and form1.is_valid():
            em=str(form.cleaned_data['email'])
            if User.objects.filter(email=em).exists():
                messages.info(request,"Email is already exists")
                return redirect(reverse('sign-up'))
            form=form.cleaned_data
            form['username']=form['username'].lower()
            u=User.objects.create_user(**form)
            form1=form1.cleaned_data
            f=follow.objects.create(user=u,profile=form1['profile'],description=form1['description'])
            People.objects.create(username=form['username'],users=u,profile=form1['profile'],description=form1['description'],follow=f)
            return HttpResponseRedirect(reverse('login'))
    content={'forms':form,'form1':form1}
    return render(request,'signup.html',content)
def login(request):
    form=loginform()
    if request.method=='POST':
        form=loginform(request.POST)
        if form.is_valid():
            user=auth.authenticate(**form.cleaned_data)
            if user:
                auth.login(request,user)
                _user=get_object_or_404(follow,user=request.user)
                _user.status1=True
                _user.save()
                return HttpResponseRedirect(reverse('data'))
            else:
                messages.info(request,"Incorrect detailes")
    content={'forms':form}

    return render(request,'login.html',content)
@login_required
def updatedata(request,pk):
    obj=get_object_or_404(People,id=pk)
    form=PeopleForm(request.POST or None,request.FILES or None,instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('data'))
    content={'forms':form}
    return render(request,'datacollect.html',content)
@login_required
def logout(request):
    _user=get_object_or_404(follow,user=request.user)
    _user.status1=False
    _user.save()
    auth.logout(request)
    return redirect('/')
@login_required
def liked(request,pk):
    ob=get_object_or_404(People,id=pk)
    likers=ob.likes_users.all()
    if request.user in likers:
        ob.likes_users.remove(request.user)
        lc=ob.counters()
        is_likers=False
    else:
        ob.likes_users.add(request.user)
        lc=ob.counters()
        is_likers=True
    resp={
        'likers':is_likers,
        'likes_count':lc
    }
    response=json.dumps(resp)

    return HttpResponse(response,content_type="application/json")
@login_required
def follows(request,pk):
    ob=get_object_or_404(People,id=pk)
    f1=get_object_or_404(follow,user=ob.users)
    f2=get_object_or_404(follow,user=request.user)
    if not f1.user in f2.followed_users():
        f2.following_users.add(f1.user)
        f2.save()
        f1.followers_users.add(request.user)
        f1.save()
        is_follow=True
    else:
        f2.following_users.remove(f1.user)
        f2.save()
        f1.followers_users.remove(request.user)
        f1.save()
        is_follow=False
    resp={
        'followers':is_follow,
        'active_user':str(request.user),
        'followers_counts_active':f1.followers_count()
        }
    print(f2.followers_count())
    response1=json.dumps(resp)

    return HttpResponse(response1,content_type="application/json")
@login_required
def profat(request,name):
    ob=get_object_or_404(User,username=name.lower())
    return profiles(request,ob.pk)
@login_required
def profiles(request,pk):
    ob=get_object_or_404(User,id=pk)
    obj={
        'ob':ob,
    }
    return render(request,'profile1.html',obj)
@login_required
def comment_post(request):
    cmt=request.GET['cmt']
    pk=request.GET['id']
    obj_post=get_object_or_404(People,id=pk)
    c=comments.objects.create(post=obj_post,user=request.user,comment=cmt)
    names=[{'names':c.user.username,'img':c.user.profile_user.profile.url,'comment':c.comment,'time':str(c.comment_date)}]
    print("runn")
    return JsonResponse(names,safe=False)
def get_comment(request):
    pk=request.GET['id']
    obj_post=get_object_or_404(People,id=pk)
    cmt=obj_post.comment_user.all()
    names=[]
    for c in cmt:
        vals={'names':c.user.username,'img':c.user.profile_user.profile.url,'comment':c.comment,'time':str(c.comment_date)}
        names.append(vals)
    print("runn")
    print(id)
    return JsonResponse(names,safe=False)


def discover(request):
    obj=People.objects.all()
    obj=list(obj.order_by('?'))
    global obj_for_ajax_discover_sug
    obj_for_ajax_discover_sug=obj[12:]
    objs={'obj':obj[:12]}
    return render(request,'discover.html',objs)
def search(request,hashtags):
    objs=People.objects.all()
    cmt_user=comments.objects.all()
    obj=[]
    hashtags=hashtags.lower()
    print(hashtags)
    h=get_object_or_404(hashtag,tag=hashtags)
    obj=h.post.all()
    obj_fol=follow.objects.all()
    if request.user.is_authenticated:
        objs={'obj':obj,'loginuser':str(request.user),'cmt_user':cmt_user}
    else:
        objs={'obj':obj}
    return render(request,'index.html',objs)
import re
def hashtagfinder(obj):
    return re.findall(r'#(\w+)',obj)
@login_required
def suggestion(request,pk):
    ob=get_object_or_404(People,id=pk)
    hashtags=hashtagfinder(ob.description.lower())
    for tag in hashtags:
        h=get_object_or_404(hashtag,tag=tag)
        h.suggest_tag.add(request.user)
@login_required
def suggest_discover(request,id):
    suggestion(request,pk=id)
    post_obj=People.objects.filter(id=id)
    hashtags=hashtagfinder(post_obj[0].description.lower())
    obj=People.objects.none()
    for tag in hashtags:
        h=get_object_or_404(hashtag,tag=tag)
        obj=obj.union(h.post.all())
    obj=list(obj)
    if post_obj[0] in obj:
        obj.remove(post_obj[0])
    obj.append(post_obj[0])
    obj=obj[::-1]
    cmt_user=comments.objects.all()
    objs={'obj':obj[:3],'cmt_user':cmt_user}
    global ajax_suggest_discover
    ajax_suggest_discover=obj[3:]
    return render(request,'index.html',objs)

def returnall(request):
    obj=People.objects.all()[0]
    from django.core import serializers
    response=serializers.serialize("json", People.objects.all())
    response={
        'data':response
    }
    response1=json.dumps(response)
    return HttpResponse(response1,content_type="application/json")
@login_required
def chat_dashboard(request):
    objs=People.objects.all()
    followers=request.user.profile_user.followers_users.all()
    followings=request.user.profile_user.following_users.all()
    followings=followings.union(followers)
    if followings:
        print("run")
        room_name=followings[0].username
        return room(request,room_name)
    else:
        return HttpResponseRedirect(reverse('data'))
@login_required
def chat(request,id):
    objs=People.objects.all()
    chat_user=get_object_or_404(User,id=id)
    print(chat_user)
    objs={
        'obj':objs,
        'chat_user':chat_user
    }
    return render(request,'chat.html',objs)
def autocomplete(request):
    print(request.is_ajax())
    if 'term' in request.GET and request.GET['term']:
        term=request.GET['term']
        names=User.objects.filter(username__icontains=term)
        names=names.union(User.objects.filter(first_name__icontains=term))[:10]
        lis=[]
        for i in names:
            d={}
            d['names']=i.username
            d['img']=i.profile_user.profile.url
            d['fullname']=i.get_full_name()
            lis.append(d)
        return JsonResponse(lis,safe=False)
    return JsonResponse([],safe=False)
