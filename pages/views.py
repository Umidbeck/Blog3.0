from django.views.generic import TemplateView, ListView, DetailView
from .models import Post, Category, Hashtag
from django.shortcuts import redirect
from .forms import CommentForm


class HomePageView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'  # Bosh sahifada oxirgi postlarni ko'rsatish
    ordering = ['-date']  # Yangilanish tartibi


class AboutPageView(TemplateView):
    template_name = 'about.html'


class ContactPageView(TemplateView):
    template_name = 'contact.html'


class DetailPageView(DetailView):
    model = Post
    template_name = 'post-details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hashtags'] = self.object.hashtags.all()  # Hashtaglarni olish
        context['comments'] = self.object.comments.all()  # Izohlarni olish
        context['form'] = CommentForm()  # Izoh formasi
        context['all_posts'] = Post.objects.all()  # Barcha postlarni olish
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=self.object.pk)
        return redirect('post_detail', pk=self.object.pk)


class BlogPageView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'  # Blog sahifasidagi postlar
    ordering = ['-date']  # Yangilanish tartibi
    paginate_by = 6


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'  # Qidiruv natijalari uchun template
    context_object_name = 'posts'
    paginate_by = 5  # Har bir sahifada ko'rsatiladigan postlar soni

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query = query.lower()  # Kichik harfga o'tkazish
            return Post.objects.filter(title__icontains=query)
