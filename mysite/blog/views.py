from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin #in CBV you have to use mixins to us decorators such as @loginrequired
from blog.forms import PostForm,CommentForm#importing forms
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy #
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from blog.models import Post,Comment
# Create your views here.
class AboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):
    model=Post

    def get_queryset(self):#python version of sqlquery
        #it says grab post model all the objects and filter the stuff in paranthesis
        #lte=less than equal to
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model=Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html' #means redirect them to the detail view
    form_class=PostForm

    model=Post

class PostUpdateView(LoginRequiredMixin,UpdateView):#same as CreatePostView because its like you creating a post
    login_url='/login/'
    redirect_field_name='blog/post_detail.html' #means redirect them to the detail view
    form_class=PostForm

    model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')#waitss until you delete a post then  gives you the success_url

#a view for unpublished class
class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


#################################################################
#################################################################

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)

    else:
        form=CommentForm()

    return render(request,'blog/comment_form.html',{'form':form}) #injecting a form dictionary to comment_form.html

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve() #if you go to the Comment models the method approve is called
    return redirect('post_detail',pk=comment.post.pk) #what is the primary key of the post that the comment is linked to

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk) #returning with post_pk because its not gonna remember the extra variable
