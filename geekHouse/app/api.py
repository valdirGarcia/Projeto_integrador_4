import requests
from django.conf import settings
from .models import Filme

# Mapeamento de IDs para nomes de gêneros
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
    # Adicione outros gêneros conforme necessário
}

def buscar_filmes(limite=50):
    """Busca filmes populares da API do TMDB."""
    api_key = settings.TMDB_API_KEY
    url = f'{settings.TMDB_API_URL}/movie/popular?api_key={api_key}&language=pt-BR&page=1'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para códigos de status 4xx e 5xx
        return response.json()['results'][:limite]  # Retorna apenas o número limitado de filmes
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Erro ao buscar dados: {err}")
    
    return []  # Retorna uma lista vazia em caso de erro

def atualizar_filmes(limite=50):
    """Atualiza o banco de dados com filmes populares."""
    filmes = buscar_filmes(limite)

    if not filmes:  # Verifica se a lista de filmes está vazia
        print("Nenhum filme encontrado.")
        return

    for filme_data in filmes:
        # Converter IDs de gênero em nomes
        generos_ids = filme_data.get('genre_ids', [])
        generos_nomes = [GENERO_MAP.get(str(g_id), str(g_id)) for g_id in generos_ids]
        genero_formatado = ', '.join(generos_nomes)

        filme, created = Filme.objects.update_or_create(
            titulo=filme_data['title'],
            defaults={
                'descricao': filme_data['overview'],
                'director': 'Desconhecido',  # Você pode adicionar lógica para obter o diretor se necessário
                'genero': genero_formatado,
                'ano': int(filme_data['release_date'][:4]),
                'imagem_url': f"https://image.tmdb.org/t/p/w500{filme_data['poster_path']}",
            }
        )

    print(f'{len(filmes)} filmes atualizados no banco de dados!')
