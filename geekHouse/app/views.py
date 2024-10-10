from django.shortcuts import render, get_object_or_404
from .models import Filme

def index(request):
    genero = request.GET.get('genero')
    if genero:
        filmes = Filme.objects.filter(genero__icontains=genero)
    else:
        filmes = Filme.objects.all()[:10]  # Retornar os primeiros 10 filmes se não houver busca

    return render(request, "index.html", {'filmes': filmes})

def detalhes_filme(request, pk):
    filme = get_object_or_404(Filme, pk=pk)  # Tenta encontrar o filme pelo ID
    return render(request, 'detalhes_filme.html', {'filme': filme})
