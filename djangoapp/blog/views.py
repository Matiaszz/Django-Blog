from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
PER_PAGE = 9


def index(request):
    posts = Post.objects.get_published()  # type:ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_title': 'Início - ',
            'page_obj': page_obj,
        }
    )


def created_by(request, author_id):
    user = User.objects.filter(id=author_id).first()

    if user is None:
        raise Http404()

    posts = Post.objects.get_published().filter(  # type:ignore
        created_by__id=author_id)

    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'

    page_title = 'Posts de ' + user_full_name + ' - '

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(  # type:ignore
        category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(posts) == 0:
        raise Http404()

    page_title = f'Categoria - {page_obj[0].category.name} - '
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


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
