from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, 
                                DetailView, 
                                CreateView,
                                UpdateView,
                                DeleteView )
from .models import Post

def home(request):
    data = {
        "posts": Post.objects.all()
    }
    return render(request, "blog/home.html", data)

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html" #convention(if you dont add this line) ->template_name = blog/post_list.html
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html" 
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted") 

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs["pk"])
        liked = False
        if likes_connected.like.filter(id=self.request.user.id).exists():
            liked = True
        data["number_of_likes"] = likes_connected.total_likes()
        data["post_is_liked"] = liked
        return data

def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    return HttpResponseRedirect(reverse("post-detail", args=[str(pk)]))

def post_dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.dislike.filter(id=request.user.id).exists():
        post.dislike.remove(request.user)
    else:
        post.dislike.add(request.user)
    return HttpResponseRedirect(reverse("post-detail", args=[str(pk)]))
    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
 
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"
   
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
def about(request):
    return render(request, "blog/about.html")