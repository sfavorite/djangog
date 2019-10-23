from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.utils import timezone 
from .models import Post 
from .forms import PostForm
from django.shortcuts import redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate, login


def user_login(request):

	if request.method == "POST":
		username = request.POST['username']
		print(username)
		
		password = request.POST['password']
		print(password)
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('post_list')
			#return  HttpResponse('logged in')
			
		else:
			# Return an 'invalid login' error message.
			return  HttpResponse('try again dumbass', status=200)
			
	else:
		form = AuthenticationForm()

		
	return render(request, 'blog/login.html', {'form': form})

def user_logout(request):
	logout(request)
	return redirect('post_list') 

# Index page with all published posts 
def post_list(request):

	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	
	return render(request, 'blog/post_list.html', {'posts': posts})

# Page to view an individual post 
def post_detail(request, pk):
	
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})


# Page to create a new post 
def post_new(request):
	
	if request.method == "POST":
		form = PostForm(request.POST)
		
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save() 
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

# Edit an existing post 
def post_edit(request, pk):

	print(request.user.id)
	if request.user.is_authenticated:

		post = get_object_or_404(Post, pk=pk)

		# Is the post author the same as the logged in user  
		
		if (request.method == "POST") and (post.author_id == request.user.id):
			form = PostForm(request.POST, instance=post)
			if form.is_valid():
				post = form.save(commit=False)
				post.author = request.user
				post.published_date = timezone.now() 
				post.save()
				return redirect('post_detail', pk=post.pk)
		else:
			form = PostForm(instance=post)
	
	return render(request, 'blog/post_edit.html', {'form': form})


from django.contrib.auth.models import User 

def new_user(request):
	user = User.objects.get(username__exact='test')
	user.set_password('testtest')
	user.save()

	return redirect('post_list')