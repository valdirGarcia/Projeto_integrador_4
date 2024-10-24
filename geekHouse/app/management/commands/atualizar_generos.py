import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Filme

# Dicionário para mapear IDs de gêneros para nomes
GENERO_MAP = {
    '28': 'Ação',
    '12': 'Aventura',
    '35': 'Comédia',
    '18': 'Drama',
    '10749': 'Romance',
    '878': 'Ficção Científica',
    '10751': 'Família',
    '16': 'Animação',
    '80': 'Crime',
    '27': 'Terror',
    '10402': 'Música',
    '10770': 'Filme de TV',
    # Adicione mais gêneros conforme necessário
}

class Command(BaseCommand):
    help = 'Atualiza os gêneros dos filmes existentes no banco de dados'

    def handle(self, *args, **kwargs):
        filmes = Filme.objects.all()  # Obtém todos os filmes

        for filme in filmes:
            # Divide os gêneros por vírgula, assumindo que eles estão armazenados como IDs
            generos_ids = filme.genero.split(', ') if filme.genero else []
            generos_nomes = [GENERO_MAP.get(g_id.strip(), g_id.strip()) for g_id in generos_ids]  # Mapeia os IDs
            novo_genero = ', '.join(generos_nomes)  # Cria uma string com os nomes dos gêneros
            
            # Atualiza o campo de gênero
            filme.genero = novo_genero
            filme.save()

        print(f'{len(filmes)} filmes atualizados com os novos gêneros!')
