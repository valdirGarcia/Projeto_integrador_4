import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Filme

class Command(BaseCommand):
    help = 'Atualiza as capas dos filmes já adicionados no banco de dados'

    def handle(self, *args, **kwargs):
        self.atualizar_capas()

    def atualizar_capas(self):
        """Atualiza as capas dos filmes no banco de dados."""
        api_key = settings.TMDB_API_KEY
        base_url = settings.TMDB_API_URL

        filmes = Filme.objects.filter(capa_url__isnull=True)  # Atualiza apenas filmes sem capa
        total = filmes.count()

        if total == 0:
            print("Nenhum filme sem capa encontrado para atualizar.")
            return

        atualizados = 0

        for filme in filmes:
            url = f"{base_url}/movie/{filme.id_filme_tmdb}?api_key={api_key}&language=pt-BR"  # Usando id único do TMDB
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    dados = response.json()
                    if 'backdrop_path' in dados and dados['backdrop_path']:
                        filme.capa_url = f"https://image.tmdb.org/t/p/w1280{dados['backdrop_path']}"
                        filme.save()
                        atualizados += 1
                        print(f"Atualizada capa do filme: {filme.titulo}")
                else:
                    print(f"Erro ao buscar dados do filme {filme.titulo}: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Erro ao processar o filme {filme.titulo}: {e}")

        print(f"Capas atualizadas: {atualizados}/{total}")
