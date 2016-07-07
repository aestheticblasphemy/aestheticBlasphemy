import django.dispatch as dispatch

comment_approved = dispatch.Signal(providing_args=['comment'])

from comments.models import Comment
from django.dispatch import receiver

@receiver(comment_approved, sender=Comment)
def comment_approved_action(sender, **kwargs):
	print 'Inside comment approved action'
	for comment in kwargs['comment']:
		comment.published = True
		comment.save()
