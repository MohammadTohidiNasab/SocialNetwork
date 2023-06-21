from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class HomeView(View):
	form_class = PostSearchForm

	def get(self, request):
		posts = Post.objects.all()
		if request.GET.get('search'):
			posts = posts.filter(body__contains=request.GET['search'])
		return render(request, 'home/index.html', {'posts':posts, 'form':self.form_class})



class PostDetailView(View):
	form_class = CommentCreateForm
	form_class_reply = CommentReplyForm

	def setup(self, request, *args, **kwargs):
		self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
		return super().setup(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		comments = self.post_instance.pcomments.filter(is_reply=False)
		can_like = False
		if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
			can_like = True
		return render(request, 'home/detail.html', {'post':self.post_instance, 'comments':comments, 'form':self.form_class, 'reply_form':self.form_class_reply, 'can_like':can_like})

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.user = request.user
			new_comment.post = self.post_instance
			new_comment.save()
			messages.success(request, 'your comment submitted successfully', 'success')
			return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)



class PostDeleteView(LoginRequiredMixin, View):
	def get(self, request, post_id):
		post = get_object_or_404(Post, pk=post_id)
		if post.user.id == request.user.id:
			post.delete()
			messages.success(request, 'post deleted successfully', 'success')
		else:
			messages.error(request, 'you cant delete this post', 'danger')
		return redirect('home:home')
