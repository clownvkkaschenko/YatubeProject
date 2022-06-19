from django.core.paginator import Paginator


LMT_PSTS: int = 10


def paginator(request, posts):
    paginator = Paginator(posts, LMT_PSTS)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
