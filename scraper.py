# Esse arquivo é responsável por:

# Acessar o site --> Extrair as informações --> Armazenar no Banco de dados

# requests --> baixar o HTML
# BeautifulSoup --> extrair os dados
# sqlite3 --> armazenar os dados

import requests
from bs4 import BeautifulSoup
import sqlite3


# Criando uma conexão com o banco de dados
conn = sqlite3.connect('dados.db')

# Criando cursor que permite executar comandos SQL
cursor = conn.cursor()

# Criando a tabela 'livros'
cursor.execute('''
CREATE TABLE IF NOT EXISTS livros(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT,
  preco TEXT  
)
''')
conn.commit()


# Função que coleta os livros do site

def coletar_livros():
    # Definimos o site de onde vamos coletar os dados
    url = "https://books.toscrape.com/"
    # Fz uma requisição HTTP(get) e pega o conteúdo da página
    response = requests.get(url)

    # Converter o html em um objeto que podemos navegar e buscar
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscamos todos os blocos de livro no html.
    livros = soup.find_all("article", class_="product_pod")
    # Cada livro está dentro de uma <article class="product_´pd"

    for livro in livros:
        titulo = livro.h3.a['title']
        preco = livro.find('p', class_='price_color').text

        cursor.execute(
            "INSERT INTO livros(titulo, preco) VALUES(?, ?)", (titulo, preco))

    conn.commit()
    print("Dados coletados com sucesso!")


if __name__ == "__main__":
    coletar_livros()
    conn.close()
