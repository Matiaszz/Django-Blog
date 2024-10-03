from django.db import models
from utils.rands import new_slugfy
from django.contrib.auth.models import User


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None,
                            blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugfy(self.name, 5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None,
                            blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugfy(self.name, 5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=65)
    slug = models.SlugField(unique=True, default='',
                            blank=True, null=False, max_length=255)
    is_published = models.BooleanField(
        default=False,
        help_text=('Este campo precisará estar '
                   'marcado para a página ser exibida publicamente.')
    )

    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugfy(self.title, 5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=65)
    slug = models.SlugField(unique=True, default='',
                            blank=True, null=False, max_length=255)

    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False,
        help_text=('Este campo precisará estar '
                   'marcado para o post ser exibido publicamente.')
    )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text=(
            'Exibe a imagem da capa dentro do conteúdo do'
            'post se marcado'
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # user.post_created_by.all()
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='post_created_by')

    # user.post_updated_by.all()
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='post_updated_by')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
    )
    tag = models.ManyToManyField(
        Tag,
        blank=True, default=''
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugfy(self.title, 5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
