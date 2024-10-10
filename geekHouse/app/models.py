from django.db import models

class Filme(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    director = models.CharField(max_length=255)
    genero = models.CharField(max_length=100)
    ano = models.IntegerField()
    imagem = models.ImageField(upload_to='filmes_imagens/', blank=True, null=True)  # Imagens locais
    imagem_url = models.URLField(max_length=500, blank=True, null=True)  # Imagens via URL

    def __str__(self):
        return self.titulo
