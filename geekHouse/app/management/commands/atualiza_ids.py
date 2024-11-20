import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Filme

class Command(BaseCommand):
    help = 'Atualiza os IDs do TMDB para filmes já existentes no banco de dados'

    def buscar_id_tmdb(self, titulo):
        """Busca o ID do TMDB para um filme baseado no título."""
        api_key = settings.TMDB_API_KEY
        base_url = settings.TMDB_API_URL
        url = f"{base_url}/search/movie?api_key={api_key}&language=pt-BR&query={titulo}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                resultados = dados.get('results', [])
                if resultados:
                    return resultados[0]['id']  # Retorna o ID do primeiro resultado
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar ID do TMDB para {titulo}: {e}")

        return None  # Retorna None se não encontrar o filme

    def handle(self, *args, **kwargs):
        filmes = Filme.objects.filter(id_filme_tmdb__isnull=True)  # Seleciona filmes sem ID
        total_filmes = filmes.count()
        atualizados = 0

        print(f"Atualizando IDs para {total_filmes} filmes...")

        for filme in filmes:
            id_tmdb = self.buscar_id_tmdb(filme.titulo)
            if id_tmdb:
                filme.id_filme_tmdb = id_tmdb
                filme.save()
                atualizados += 1
                print(f"Atualizado: {filme.titulo} - ID TMDB: {id_tmdb}")
            else:
                print(f"Não foi possível encontrar o ID para: {filme.titulo}")

        print(f"Atualização concluída! {atualizados} filmes atualizados com sucesso.")
