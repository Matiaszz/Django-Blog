from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
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


class TagListView(PostListView):
    def get_queryset(self):
        qs = super().get_queryset().filter(tag__slug=self.kwargs.get('slug'))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tag_obj = self.object_list[0].tag.first().name  # type: ignore
        page_title = f'Tag - {tag_obj} - '
        ctx.update({'page_title': page_title})
        return ctx


class SearchListView(PostListView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value

        qs = super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[0:PER_PAGE]

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'Pesquisa - {self._search_value[:30]} - '

        ctx.update({'page_title': page_title})
        ctx.update({'search_value': self._search_value})

        return ctx

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)


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
