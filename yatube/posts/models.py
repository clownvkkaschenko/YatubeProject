from core.models import CreatedModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Class for creating groups."""
    title = models.CharField('Имя сообщества', max_length=200)
    slug = models.SlugField('Адрес сообщества', unique=True)
    description = models.TextField('Описание сообщества')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(CreatedModel):
    """Class for creating posts."""
    text = models.TextField(
        'Текст поста',
        help_text='Текст вашего поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='group_list',
        verbose_name='Сообщество поста',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Class for creating comments."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Текст поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Напишите свой комментарий, но учтите, '
        'что вы не сможете изменить его.'
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    """Class for subscribing to authors."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор на которого подписываются'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_object'
            ),
        ]
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
