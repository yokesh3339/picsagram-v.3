from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User,auth,AbstractUser
from django.shortcuts import render,redirect,get_object_or_404
from cloudinary.models import CloudinaryField
# Create your models here.
""" user profile model"""
class follow(models.Model):
    user=models.OneToOneField(User,related_name="profile_user",on_delete=models.CASCADE)
    followers_users=models.ManyToManyField(User,related_name='followers',blank=True)
    following_users=models.ManyToManyField(User,related_name='followings',blank=True)
    description=models.TextField(max_length=100,blank=True,null=True,default="No Description Available")
    #profile=models.ImageField(upload_to='profiles',blank=True,default="profiles/default.jpg")
    profile=CloudinaryField('profile_image')
    suggested_tag=models.TextField(blank=True,null=True)
    status=models.BooleanField(default=False)
    status1=models.BooleanField(default=False)
    def __str__(self):
        return str(self.pk) + " | " + str(self.user) 
    def followed_users(self):
        my_followers=self.following_users.all()
        return my_followers
    def followers(self):
        my_followers=self.followers_users.all()
        return my_followers
    def followed_users_count(self):
        my_followers=self.following_users.all().count()
        return my_followers
    def followers_count(self):
        my_followers=self.followers_users.all().count()
        return my_followers
class People(models.Model):
    username=models.CharField(max_length=20)
    #firstname=models.CharField(max_length=50)
    #lastname=models.CharField(max_length=50)
    users=models.ForeignKey(User,related_name="post_user",on_delete=models.CASCADE)
    description=models.TextField(max_length=100,blank=True,null=True,default="No Description Available")
    #profile=models.ImageField(upload_to='pics',blank=True,default="profiles/default.jpg")
    profile=CloudinaryField('profile')
    likes=models.BooleanField(default=False)
    no_down=models.IntegerField(default=0,blank=True)
    likes_users=models.ManyToManyField(User,related_name='blog_post',blank=True)
    follow=models.ForeignKey(follow,related_name="follow",on_delete=models.CASCADE,default=1)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.pk) + " | " + self.username 
    def get_absolute_url(self):
        return reverse("listing", kwargs={'my_username': self.username})
    def get_absolute_urls(self):
        return reverse("specific-view", kwargs={'pk':self.pk})
    def get_likes_url(self):
        return reverse("liked", kwargs={"pk": self.pk})
    def counters(self):
       return self.likes_users.count()
    def down_counts(self):
        self.no_down+=1
        return self.no_down
    def reverse_obj(self):
        obj=People.objects.all()[::-1]
        return obj
    def likedusers(self):
        a=self.likes_users.all()
        #lis=[str(i) for i in a]
        #return lis
        return a
    def get_username(self):
        u=User.objects.all()
        lis=[str(i) for i in u]
        return lis
class comments(models.Model):
    post=models.ForeignKey(People,related_name='comment_user',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    comment=models.TextField()
    comment_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.pk)+" | " + str(self.post) + " | " + str(self.user)
    def get_all_comments(self):
        obj=self.objects.all()
        return obj.order_by("comment_date")
class hashtag(models.Model):
    tag=models.CharField(max_length=30,blank=True)
    post=models.ManyToManyField(People,related_name='tag_post',blank=True)
    suggest_tag=models.ManyToManyField(User,related_name="suggest",blank=True )

    def __str__(self):
        return str(self.id) + "|" + self.tag 
    
    