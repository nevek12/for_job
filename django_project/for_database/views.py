from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView
def news_home(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'for_database/news_home.html', {'news': news})
# Create your views here.
class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'for_database/create.html'
    form_class = ArticlesForm
class NewsDetailView(DetailView):
    model = Articles
    template_name = 'for_database/details_view.html'
    context_object_name = 'article'
def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'
    form = ArticlesForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'for_database/create.html', data)