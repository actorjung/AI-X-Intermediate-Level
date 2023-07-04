from django.shortcuts import render, redirect

from django_project.settings import BAD_WORDS,SLANG_WORDS,MIM_WORDS
from .models import Post, Category, Tag, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .baggle import Baggle

# 매개변수랑 render에 첫번째 인자는 request 외워
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/post_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            # 업데이트 권환 확인
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tags']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_staff):
            form.instance.author = self.request.user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')
        # 매번 보내는 것보단 해당하는 오류에 대해 알려주는 게 좋음

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostList(ListView):
    model = Post
    ordering = '-pk'
    paginate_by = 5

    # 오버라이드
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment'] = CommentForm
        return context


def categories_page(request, slug):
    if slug == 'no-category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        'category': category,
        'categories': Category.objects.all(),
        'post_list': post_list,
        'no_category_post_count': Post.objects.filter(category=None).count()
    }
    return render(request, 'blog/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        'tag': tag,
        'categories': Category.objects.all(),
        'post_list': post_list,
        'no_category_post_count': Post.objects.filter(category=None).count()
    }
    return render(request, 'blog/post_list.html', context)


def add_comment(request, pk):
    if not request.user.is_authenticated:
        raise PermissionError
    else:
        if request.method == 'POST':
            post = Post.objects.get(pk=pk)
            comment_form = CommentForm(request.POST)
            comment_temp = comment_form.save(commit=False)
            comment_temp.original_content = comment_temp.content
            comment_temp.post = post
            comment_temp.author = request.user

            baggle = Baggle(BAD_WORDS,SLANG_WORDS,MIM_WORDS)  # 욕설 단어 리스트 설정

            # 댓글 처리 및 출력 값 얻기
            step22_result, step33_result, step44_result = baggle.process_comments(comment_temp.content)
            comment_temp.step22_result=step22_result
            comment_temp.step33_result=step33_result
            comment_temp.step44_result=step44_result
            comment_temp.save()

            return redirect(post.get_absolute_url())
        else:
            raise PermissionError

def add_aggression(request, pk):
    if not request.user.is_authenticated:
        raise PermissionError
    else:
        if request.method == 'POST':
            post = Post.objects.get(pk=pk)
            comment_form = CommentForm(request.POST)
            comment_temp = comment_form.save(commit=False)
            comment_temp.post = post
            comment_temp.author = request.user

            comment_temp.aggression=comment_temp.content
            baggle = Baggle(BAD_WORDS,SLANG_WORDS,MIM_WORDS)  # 욕설 단어 리스트 설정

            # 댓글 처리 및 출력 값 얻기
            analyze_comment = baggle.process_advisor(comment_temp.content)

            return render(request,'blog/aggression_check.html',{'analyze_comment':analyze_comment,'post':post,'comment':comment_temp,'comment_form':comment_form})
        else:
            raise PermissionError

class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionError

def get_original_content_me(request):
    # 게시물 정보 가져오기
    author = request.user
    posts = Post.objects.filter(author=author)
    comments = Comment.objects.filter(post__in=posts)

    # 내가 쓴 게시물의 댓글은 step22_result로 대체
    for comment in comments:
        comment.content = comment.original_content
        comment.save()

    request.session['previous_step1'] = '적용안함'
    previous_step11 = request.session.get('previous_step2')

    redirect_url = '/blog/?now_step=적용안함&now_step2={}'.format(request.GET.get('now_step2')or previous_step11)
    return redirect(redirect_url)

def get_step22_results_me(request):
    # 게시물 정보 가져오기
    author = request.user
    posts = Post.objects.filter(author=author)
    comments = Comment.objects.filter(post__in=posts)

    # 내가 쓴 게시물의 댓글은 step22_result로 대체
    for comment in comments:
        comment.content = comment.step22_result
        comment.save()

    request.session['previous_step1'] = '1단계'
    previous_step11 = request.session.get('previous_step2')

    redirect_url = '/blog/?now_step=1단계&now_step2={}'.format(request.GET.get('now_step2')or previous_step11)

    return redirect(redirect_url)

def get_step33_results_me(request):
    # 게시물 정보 가져오기
    author = request.user
    posts = Post.objects.filter(author=author)
    comments = Comment.objects.filter(post__in=posts)

    # 내가 쓴 게시물의 댓글은 step22_result로 대체
    for comment in comments:
        comment.content = comment.step33_result
        comment.save()

    request.session['previous_step1'] = '2단계'
    previous_step11 = request.session.get('previous_step2')

    redirect_url = '/blog/?now_step=2단계&now_step2={}'.format(request.GET.get('now_step2')or previous_step11)

    return redirect(redirect_url)

def get_step44_results_me(request):
    # 게시물 정보 가져오기
    author = request.user
    posts = Post.objects.filter(author=author)
    comments = Comment.objects.filter(post__in=posts)

    # 내가 쓴 게시물의 댓글은 step22_result로 대체
    for comment in comments:
        comment.content = comment.step44_result
        comment.save()

    request.session['previous_step1'] = '3단계'
    previous_step11 = request.session.get('previous_step2')

    redirect_url = '/blog/?now_step=3단계&now_step2={}'.format(request.GET.get('now_step2')or previous_step11)

    return redirect(redirect_url)


def get_original_content_other(request):
    # 게시물 정보 가져오기
    author = request.user
    posts = Post.objects.exclude(author=author)
    comments = Comment.objects.filter(post__in=posts)

    # 내가 쓴 게시물의 댓글은 step22_result로 대체
    for comment in comments:
        comment.content = comment.original_content
        comment.save()

    request.session['previous_step2'] = '적용안함'
    previous_step22 = request.session.get('previous_step1')

    redirect_url = '/blog/?now_step={}&now_step2=적용안함'.format(request.GET.get('now_step')or previous_step22)

    return redirect(redirect_url)

def get_step22_results_other(request):
    # 게시물 정보 가져오기
    author = request.user
    posts = Post.objects.exclude(author=author)
    comments = Comment.objects.filter(post__in=posts)

    # 내가 쓴 게시물의 댓글은 step22_result로 대체
    for comment in comments:
        comment.content = comment.step22_result
        comment.save()

    request.session['previous_step2'] = '1단계'
    previous_step22 = request.session.get('previous_step1')

    redirect_url = '/blog/?now_step={}&now_step2=1단계'.format(request.GET.get('now_step')or previous_step22)

    return redirect(redirect_url)

def get_step33_results_other(request):
    # 게시물 정보 가져오기
    author = request.user
    posts = Post.objects.exclude(author=author)
    comments = Comment.objects.filter(post__in=posts)

    # 내가 쓴 게시물의 댓글은 step22_result로 대체
    for comment in comments:
        comment.content = comment.step33_result
        comment.save()

    request.session['previous_step2'] = '2단계'
    previous_step22 = request.session.get('previous_step1')

    redirect_url = '/blog/?now_step={}&now_step2=2단계'.format(request.GET.get('now_step')or previous_step22)

    return redirect(redirect_url)

def get_step44_results_other(request):
    # 게시물 정보 가져오기
    author = request.user
    posts = Post.objects.exclude(author=author)
    comments = Comment.objects.filter(post__in=posts)

    # 내가 쓴 게시물의 댓글은 step22_result로 대체
    for comment in comments:
        comment.content = comment.step44_result
        comment.save()

    request.session['previous_step2'] = '3단계'
    previous_step22 = request.session.get('previous_step1')

    redirect_url = '/blog/?now_step={}&now_step2=3단계'.format(request.GET.get('now_step')or previous_step22)

    return redirect(redirect_url)

def mim_explanation(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    baggle = Baggle(BAD_WORDS,SLANG_WORDS,MIM_WORDS)
    mim = baggle.process_explain(comment.content)
    return render(request,"blog/mim.html",{"post":post,"mim":mim,"mimcomment":comment})

# 정적 FBV
# def index(request):
#    posts = Post.Objects.all()
#    return render(request,'blog/index.html'{'posts':posts})
#
# def single_post_page(request,post_num):
#    post=Post.objects.get(pk=post_num)
#    return render(request, 'blog/post_detail.html', {'post':post})
# 먼저 url 패턴에 잘 걸리는지 확인하고 함수 작성