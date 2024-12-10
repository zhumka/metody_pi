from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Comment


@receiver(post_save, sender=Comment)
def send_email_to_post_owner(sender, instance, created, **kwargs):
    if created:  # Только при создании нового комментария
        post = instance.post
        post_owner = post.author
        comment_author = instance.author
        comment_content = instance.content

        # Проверяем, есть ли у владельца поста email
        if post_owner.email:
            subject = f'Новый комментарий к вашему посту: {post.title}'
            message = (
                f'Здравствуйте, {post_owner.username}!\n\n'
                f'Пользователь {comment_author.username} оставил комментарий к вашему посту "{post.title}":\n\n'
                f'"{comment_content}"\n\n'
                f'Вы можете посмотреть комментарий здесь: http://127.0.0.1:8000/post/{post.id}/\n\n'
                f'С уважением, команда блога.'
            )
            send_mail(
                subject,
                message,
                'your_email@gmail.com',  # От кого
                [post_owner.email],  # Кому
                fail_silently=False,  # Если ошибка, уведомить
            )
