from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView

PER_PAGE = 9


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()  # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs=kwargs)

        context.update({'page_title': 'Início - '})
        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '
        ctx.update({
            'page_title': page_title,
        })
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__id=self._temp_context['user'].id)
        return qs

    def get(self, request, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        user = User.objects.filter(id=author_id).first()
        if user is None:
            raise Http404()
        self._temp_context.update({
            'author_id': author_id,
            'user': user,
        })
        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    # instead of going to the "nothing found" area, redirect to a 404 page.
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().filter(
            category__slug=self.kwargs.get('slug'))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category = self.object_list[0].category.name  # type: ignore

        page_title = f'Categoria - {category} - '
        ctx.update({'page_title': page_title})
        return ctx


def tag(request, slug):
    posts = Post.objects.get_published().filter(  # type:ignore
        tag__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(posts) == 0:
        raise Http404()
    page_title = 'Tag - ' + \
        page_obj[0].tag.filter(slug=slug).first().name + ' - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = Post.objects.get_published().filter(  # type:ignore

        Q(title__icontains=search_value) |
        Q(excerpt__icontains=search_value) |
        Q(content__icontains=search_value)
    )[0:9]

    page_title = f'Pesquisa - {search_value[:30]} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'page_title': page_title,
        }
    )


def page(request, slug):
    page_obj = (Page.objects.
                filter(is_published=True)
                .filter(slug=slug)
                .first()

                )

    if page_obj is None:
        raise Http404()

    page_title = f'Página - {page_obj.title} - '
    context = {
        'page': page_obj,
        'page_title': page_title,
    }

    return render(
        request,
        'blog/pages/page.html', context,
    )


def post(request, slug):
    post_obj = (Post.objects.get_published().filter(  # type: ignore
        slug=slug).first())
    if post_obj is None:
        raise Http404()

    page_title = f'Post - {post_obj.title} - '

    context = {
        'post': post_obj,
        'page_title': page_title,
    }

    return render(
        request,
        'blog/pages/post.html', context
    )
