# Web-Scraping-e-Banco-de-Dados-SQLite3

Este projeto realiza a extração de informações de produtos do site Loja Maeto e os armazena em um banco de dados SQLite.

--Requisitos--
Certifique-se de ter o Python instalado (versão 3.7 ou superior).

Instalação de dependências:
Recomendao o uso de um ambiente virtual:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

Em seguida, instale as bibliotecas necessárias:
pip install requests beautifulsoup4

--Configuração do Banco de Dados--
Antes de executar o scraper, é necessário criar o banco de dados SQLite. Para isso, execute o script abaixo: 
-Criando o banco de Dados-
python create_database.py (Esse comando criará um banco de dados products.db com a tabela products.)

-Executando a Aplicação-
Para iniciar o scraper e buscar produtos na Loja Maeto, execute:
                  python seu_script.py
O programa solicitará um termo de busca. Por exemplo:
            Digite o termo de busca: notebook
Se houver produtos encontrados, a saída será:
            5 produtos salvos no banco de dados.
Caso contrário:
                Nenhum produto encontrado.]

--Consultando os Dados Armazenados--
Caso queira visualizar os produtos armazenados no banco de dados SQLite, execute o seguinte script:
import sqlite3

conn = sqlite3.connect("products.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

--Estrutura do Banco de Dados--
A tabela products possui os seguintes campos:

sku (TEXT, PRIMARY KEY)

title (TEXT)

price (REAL)

price_pix (REAL)

installment_value (REAL)

installment_count (INTEGER)

technical_info (TEXT)

updated_at (TEXT)


