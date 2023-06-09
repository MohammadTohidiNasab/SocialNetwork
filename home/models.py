from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	body = models.TextField()
	slug = models.SlugField()
	title = models.CharField(max_length=100, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return f'{self.slug} - {self.updated}'

	def get_absolute_url(self):
		return reverse('home:post_detail', args=(self.id, self.slug))

	def likes_count(self):
		return self.pvotes.count()

	def user_can_like(self, user):
		user_like = user.uvotes.filter(post=self)
		if user_like.exists():
			return True
		return False

