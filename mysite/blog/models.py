from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True,null=True)#the publish date is null

    def publish(self):
        self.published_date=timezone.now() #when hitting publish it take the current time
        self.save()#the publish date is being saved

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        #this means after you have created post and you hit publication it sends the primary key to post_detail
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=200)#the author of the comment isnt the author of the post
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now())
    approved_comment=models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()

    def get_absolute_url(self):
        #once you created a comment you go back to the post_list
        return reverse('post_list')

    def __str__(self):
        return self.text
