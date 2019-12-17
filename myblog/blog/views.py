from django.shortcuts import render
from .models import Article, Category, Tui, Tag, Banner, Link
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Exists

# Create your views here.
#首页
def index(request):
    allCategory = Category.objects.all()
    allBanner = Banner.objects.filter(is_active=True)
    reComArticle = Article.objects.filter(tui__id='1').order_by('-modified_time')[:3]
    allArticle = Article.objects.all().order_by('-id')
    hotArticle = Article.objects.all().order_by('-views')[:10]
    remen = Article.objects.filter(tui__id='2').order_by('-modified_time')[:6]
    tags = Tag.objects.all()
    context = {
        'allCategory': allCategory,
        'allBanner': allBanner,
        'reComArticle': reComArticle,
        'allArticle': allArticle,
        'hotArticle': hotArticle,
        'remen': remen,
        'tags': tags
    }
    return render(request, 'index.html', context)

#列表页
def list(request,lid):
    list = Article.objects.filter(category__id=lid).order_by('-id')
    cName = Category.objects.get(pk=lid)
    allCategory = Category.objects.all()
    hotArticle = Article.objects.all().order_by('-views')[:10]
    tags = Tag.objects.all()
    remen = Article.objects.filter(tui__id='2').order_by('-modified_time')[:6]

    page = request.GET.get('page')
    paginator = Paginator(list, 2)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    return render(request, 'list.html', locals())

#内容页
def show(request,sid):
    show = Article.objects.get(pk=sid)
    allCategory = Category.objects.all()
    hotArticle = Article.objects.all().order_by('-views')[:10]
    remen = Article.objects.filter(tui__id='2').order_by('-modified_time')[:6]
    tags = Tag.objects.all()
    articleTag = show.tags.all()
    xingqu = Article.objects.filter(tags=Exists(articleTag))
    pre_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category.id).last()
    next_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    show.views += 1
    show.save()
    return render(request, 'show.html', locals())


#标签页
def tag(request, tag):
    list = Article.objects.filter(tag__id=tag).order_by('-id')
    allCategory = Category.objects.all()
    hotArticle = Article.objects.all().order_by('-views')[:10]
    tags = Tag.objects.all()
    remen = Article.objects.filter(tui__id='2').order_by('-modified_time')[:6]
    tagName = Tag.objects.get(pk=tag)

    page = request.GET.get('page')
    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    return render(request, 'tags.html', locals())

# 搜索页
def search(request):
    keyWord = request.GET.get('search')
    list = Article.objects.filter(title__contains=keyWord).order_by('-id')
    allCategory = Category.objects.all()
    hotArticle = Article.objects.all().order_by('-views')[:10]
    tags = Tag.objects.all()
    remen = Article.objects.filter(tui__id='2').order_by('-modified_time')[:6]


    page = request.GET.get('page')
    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    return render(request, 'tags.html', locals())
# 关于我们
def about(request):
    pass