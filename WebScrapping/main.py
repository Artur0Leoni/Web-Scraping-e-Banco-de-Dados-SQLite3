import sqlite3
from datetime import datetime
import requests

from bs4 import BeautifulSoup

base_url = "https://www.lojamaeto.com"
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

def search_products(term):
    url = f"{base_url}/search/?q={term}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro ao acessar o site.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.select(".product"):
        sku = item.get("data-sku", "")
        title = item.select_one(".product-list-name").text.strip()
        price = float(item.select_one(".to-price").text.replace("R$", "").replace(",", "."))

        price_pix = float(item.select_one(".cash-payment-container > .to-price").text.replace("R$", "").replace(",", ".")) if item.select_one(
            ".cash-payment-container > .to-price") else price

        installment_info = item.select_one(".installments-number").text.strip().split("x") if item.select_one(
            ".installments-amount") else ["1", str(price)]

        try:
            installment_count = int(installment_info[0])

            installment_value_str = installment_info[1].replace("R$", "").replace(",", ".").strip()
            installment_value = float(installment_value_str) if installment_value_str else price

            technical_info = get_product_detail(item)
        except ValueError:
            installment_value = price
            installment_count = 1
            technical_info = ""

        updated_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        products.append((sku, title, price, price_pix, installment_value, installment_count, technical_info, updated_at))

    return products

def get_product_detail(product_soup):
    product_detail_button = product_soup.select_one(".product-list-name > a")
    product_button_attribute = product_detail_button.get("href")
    product_detail_url = f"{base_url}{product_button_attribute}"

    product_detail_response = requests.get(product_detail_url, headers=headers)
    detail_soup = BeautifulSoup(product_detail_response.text, "html.parser")

    return detail_soup.select_one(".product-detail-description > div").text.strip()

def save_products(products):
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    for product in products:
        cursor.execute('''  
            INSERT INTO products (sku, title, price, price_pix, installment_value, installment_count, technical_info, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(sku) DO UPDATE SET
                title = excluded.title,
                price = excluded.price,
                price_pix = excluded.price_pix,
                installment_value = excluded.installment_value,
                installment_count = excluded.installment_count,
                technical_info = excluded.technical_info,
                updated_at = excluded.updated_at
        ''', product)

    conn.commit()
    conn.close()


def main():
    term = input("Digite o termo de busca: ")
    products = search_products(term)

    if products:
        save_products(products)
        print(f"{len(products)} produtos salvos no banco de dados.")
    else:
        print("Nenhum produto encontrado.")


if __name__ == "__main__":
    main()