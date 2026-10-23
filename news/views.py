from django.db.models.query import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import News
from .cache_utils import get_cached_categories_with_counts
from .forms import NewsForm


@method_decorator(cache_page(60 * 5, cache="pages"), name="dispatch")
class NewsListView(ListView):
    model = News
    template_name = "news/news_list.html"
    context_object_name = "news_list"

    def get_queryset(self):
        return News.objects.select_related("category", "author").all()


@method_decorator(vary_on_cookie, name="dispatch")
@method_decorator(cache_page(60 * 5, cache="pages"), name="dispatch")
class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = "news"

    def get_queryset(self):
        return News.objects.select_related("category", "author")


class CategoryListView(TemplateView):
    template_name = "news/category_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = get_cached_categories_with_counts()
        return context


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:news_list')
    permission_required = 'news.change_news'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm('news.can_edit_other_news'):
            return queryset

        return queryset.filter(author=self.request.user)


class NewsDeleteView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:news_list')
    permission_required = 'news.delete_news'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm('news.can_delete_other_news'):
            return queryset

        return queryset.filter(author=self.request.user)
    