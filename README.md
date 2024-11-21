# GeekHouse 🎬

**GeekHouse** é um site que permite consultar uma ampla gama de filmes de diversos gêneros. Com uma barra de pesquisa intuitiva, você pode buscar filmes por título, gênero ou diretor. Ao selecionar um filme, você obtém informações detalhadas, como sinopse, e ainda pode receber recomendações personalizadas com a ajuda de uma IA generativa.

---

## ✨ **Funcionalidades**

- 🔍 **Pesquisa Inteligente**: Busque filmes por título, gênero ou diretor.
- 📖 **Informações Detalhadas**: Exibe sinopse e outros dados relevantes sobre o filme selecionado.
- 🤖 **Recomendações Personalizadas**: O botão **"Me Recomende"** aciona a IA generativa do Gemini, que analisa o título e a descrição do filme para sugerir conteúdos semelhantes.
- 🎥 **Carrossel Interativo**: Uma interface moderna com carrosséis estilizados para destacar os filmes em exibição.

---

## 🛠️ **Tecnologias Utilizadas**

- **Backend**:
  - [Django](https://www.djangoproject.com/)
  - Python 3.x

- **APIs**:
  - [The Movie Database API (TMDb)](https://www.themoviedb.org/documentation/api)
  - **Gemini API**: Para recomendações personalizadas usando IA generativa.

- **Frontend**:
  - [Bootstrap](https://getbootstrap.com/) (com ênfase no recurso de carrossel)
  - CSS customizado

---

## 🚀 **Como Rodar o Projeto**

### **Pré-requisitos**
- Python 3.x
- Pip
- Ambiente virtual (recomendado)

### **Passos**
1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/geekhouse.git
   cd geekhouse

2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Para Linux/Mac
   venv\Scripts\activate      # Para Windows

3. Instale as dependêcias:
   ```bash
   pip install -r requirements.txt

4. Rode as migrações
   ```bash
   python manage.py migrate

5. Inicie o servidor pelo terminal
   ```bash
   python manage.py runserver

6. Acesso o site do navegador
   ```bash
   python manage.py runserver

