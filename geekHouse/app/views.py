from django.shortcuts import render, get_object_or_404
from .models import Filme
from django.db.models import Q
from django.conf import settings
import google.generativeai as genai

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


def recomendacoes(request, filme_id):
    filme = Filme.objects.get(id=filme_id)
    nome_film = filme.titulo
    descricao_film = filme.descricao
    
    # preparando o gemini
    
    genai.configure(api_key=settings.GEMINI_KEY)
    model = genai.GenerativeModel('gemini-pro')

    # Gerar recomendações com base no nome e descrição do filme
    recomendacoes_filmes = model.generate_content(f"Recomende filmes semelhantes a {nome_film}: {descricao_film}")

    return render(request, 'recomendacoes.html', {
        'filme': filme,
        'recomendacoes': recomendacoes_filmes.text
    })

