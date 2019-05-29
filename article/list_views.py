from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticlePost, Comment
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count

import redis
from django.conf import settings

### 第三次修改
from account.models import UserProfile


r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()

    paginator = Paginator(articles_title, 2)
    page = request.GET.get('page')# 获得page
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list

    if username:
        return render(request, "article/list/author_articles.html", {"articles": articles, "page": current_page, "userinfo": userinfo, "user": user})
    return render(request, "article/list/article_titles.html", {"articles": articles, "page": current_page})


def article_detail(request, id, slug):
 
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby('article_ranking', 1, article.id) # 有序集合

    article_ranking = r.zrange("article_ranking", 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    article_tags_ids = article.article_tag.values_list("id", flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:4]
    return render(request, "article/list/article_content.html",
                  {"article": article, "total_views": total_views, "most_viewed": most_viewed,  "similar_articles": similar_articles,"statue":0})

@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")  # 为什么这里没有出现跳转呢
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")



# 与comment 相关的内容
def comments(request):
    if request.method == "POST":
        article = request.POST.get("article_id")
    else:
        article = request.GET.get("article_id")
    print("前面的ajax调用了这一个函数  哎哎哎  想哭啊")
    return render(request,"article/commentform.html",{"article":article,"statue":1})

@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def like_comment(request):
    comment_id = request.POST.get("id")
    action = request.POST.get("action")
    if comment_id and action:
        try:
            article = Comment.objects.get(id=comment_id)
            if action == "like":
                Comment.users_like.add(request.user)
                return HttpResponse("1")  # 为什么这里没有出现跳转呢
            else:
                Comment.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")


@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def add_comment(request):
    # ajax article.id
    if request.method == "POST":
        id = request.POST.get("article_id")
        slug = request.POST.get("article_slug")
        article = get_object_or_404(ArticlePost, id=id, slug=slug)
        body = request.POST.get("content")
        new_comment = Comment()
        new_comment.article = article
        new_comment.commentator = request.user
        new_comment.body = body
        new_comment.save()
    return render(request,"article/commentform.html",{"article":article})


@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def del_comment(request):
    # ajax  comment id article id
    if request.method == "POST":
        id = request.POST.get("comment_id")
        article_id = request.POST.get("article_id")
        article = get_object_or_404(ArticlePost, id=id)
        comment = get_object_or_404(Comment,id)
        comment.delete()
    return render(request,"article/commentform.html",{"article":article})


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def replay_comment(request):
    if request.method == "POST":
        # ajax 返回给我的是 article_id
        # isreplaied = parent_comment_id
        # form : body created 
        article = request.POST.get("article_id")
        isreplaied = request.POST.get("isreplaied")
        comment_replay_form = CommentReplayForm(data=request.POST)
        if comment_replay_form.is_valid() and isreplaied:
            new_comment = comment_replay_form.save(commit=False)
            new_comment.commentator = request.user
            new_comment.article = article
            new_comment.isreplaied = isreplaied
            new_comment.save()


