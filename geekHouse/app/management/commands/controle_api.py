import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Filme


class Command(BaseCommand):
    help = 'Adiciona um número especificado de filmes populares do TMDB ao banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limite',
            type=int,
            default=50,
            help='Número de filmes a serem inseridos (default: 50)',
        )

    def handle(self, *args, **kwargs):
        limite = kwargs['limite']
        self.adicionar_filmes(limite)

    def buscar_filmes(self, limite=50):
        """Busca filmes populares da API do TMDB."""
        api_key = settings.TMDB_API_KEY
        url = f'{settings.TMDB_API_URL}/movie/popular?api_key={api_key}&language=pt-BR&page=1'

        try:
            response = requests.get(url)
            response.raise_for_status()  # Levanta um erro se a resposta não for 200

            return response.json()['results'][:limite]  # Retorna apenas o número limitado de filmes
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP: {http_err}")
        except Exception as err:
            print(f"Erro: {err}")
        
        return []

    def adicionar_filmes(self, limite=50):
        """Adiciona filmes populares ao banco de dados."""
        filmes = self.buscar_filmes(limite)

        for filme_data in filmes:
            genero = ', '.join([str(g) for g in filme_data['genre_ids']])
            # Usa create para adicionar novos filmes
            Filme.objects.create(
                titulo=filme_data['title'],
                descricao=filme_data['overview'],
                director='Desconhecido',  # Você pode adicionar lógica para obter o diretor se tiver
                genero=genero,
                ano=int(filme_data['release_date'][:4]),
                imagem_url=f"https://image.tmdb.org/t/p/w500{filme_data['poster_path']}",
            )

        print(f'{len(filmes)} filmes adicionados ao banco de dados!')
