from django.shortcuts import render, get_object_or_404
from .models import Filme
from django.db.models import Q

def index(request):
    query = request.GET.get('busca')  # Mantenha o nome 'genero' na busca para compatibilidade com o front-end

    if query:
        filmes = Filme.objects.filter(
            Q(genero__icontains=query) |
            Q(titulo__icontains=query) |
            Q(director__icontains=query)
        )
    else:
        filmes = Filme.objects.all()[:10]  

    return render(request, "index.html", {'filmes': filmes})


def detalhes_filme(request, pk):
    filme = get_object_or_404(Filme, pk=pk)  
    return render(request, 'detalhes_filme.html', {'filme': filme})
