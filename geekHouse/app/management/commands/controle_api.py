import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Filme

GENERO_MAP = {
    '28': 'Ação',
    '12': 'Aventura',
    '16': 'Animação',
    '35': 'Comédia',
    '80': 'Crime',
    '99': 'Documentário',
    '18': 'Drama',
    '10751': 'Família',
    '14': 'Fantasia',
    '36': 'História',
    '27': 'Terror',
    '10402': 'Música',
    '9648': 'Mistério',
    '10749': 'Romance',
    '878': 'Ficção Científica',
    '10770': 'Filme de TV',
    '53': 'Thriller',
    '10752': 'Guerra',
    '37': 'Ocidental',
    # Adicione mais gêneros conforme necessário
}

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
        """Busca filmes populares da API do TMDB com controle de páginação."""
        api_key = settings.TMDB_API_KEY
        url = f'{settings.TMDB_API_URL}/movie/popular?api_key={api_key}&language=pt-BR&page=1'

        filmes = []
        pagina = 1

        while len(filmes) < limite:
            response = requests.get(f"{url}&page={pagina}")
            if response.status_code != 200:
                print(f"Erro ao buscar filmes: {response.status_code}")
                break

            dados = response.json()
            filmes.extend(dados['results'])

            if len(dados['results']) == 0:  # Se não houver mais filmes, sai do loop
                break

            pagina += 1

        return filmes[:limite]

    def obter_diretor(self, filme_id):
        """Obtém o nome do diretor de um filme usando seu ID na API do TMDB."""
        api_key = settings.TMDB_API_KEY
        url = f'{settings.TMDB_API_URL}/movie/{filme_id}/credits?api_key={api_key}&language=pt-BR'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                for membro in dados['crew']:
                    if membro['job'] == 'Director':
                        return membro['name']
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter o diretor: {e}")
        
        return 'Desconhecido'  # Retorna 'Desconhecido' caso não encontre o diretor

    def adicionar_filmes(self, limite=50):
        """Adiciona filmes populares ao banco de dados, evitando duplicações e melhorando a performance."""
        filmes = self.buscar_filmes(limite)
        filmes_a_adicionar = []

        for filme_data in filmes:
            # Verifica se o filme já existe no banco de dados
            if Filme.objects.filter(titulo=filme_data['title']).exists():
                continue

            # Obtém o diretor usando a função obter_diretor
            diretor = self.obter_diretor(filme_data['id'])
            
            # Converte os IDs dos gêneros para seus nomes usando o GENERO_MAP
            generos = [GENERO_MAP.get(str(g), 'Desconhecido') for g in filme_data['genre_ids']]
            genero = ', '.join(generos)
            
            # Verifica se a data de lançamento não está vazia antes de converter
            ano_str = filme_data['release_date']
            ano = int(ano_str[:4]) if ano_str else 0  # Se a data estiver vazia, define como None

            filme = Filme(
                titulo=filme_data['title'],
                descricao=filme_data['overview'],
                director=diretor,
                genero=genero,
                ano=ano,  # Usando o ano corretamente aqui
                imagem_url=f"https://image.tmdb.org/t/p/w500{filme_data['poster_path']}",
            )

            filmes_a_adicionar.append(filme)

        # Inserindo filmes de forma otimizada
        if filmes_a_adicionar:
            Filme.objects.bulk_create(filmes_a_adicionar)
            print(f'{len(filmes_a_adicionar)} filmes adicionados ao banco de dados!')
        else:
            print('Nenhum filme novo foi adicionado.')
