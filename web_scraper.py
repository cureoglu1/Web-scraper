from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search = request.form.get('search', '')
        url = f"https://www.trendyol.com/sr?q={search}"

        # Send a GET request
        response = requests.get(url)
        html_content = response.content

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract product names and prices
        product_names = soup.find_all("span", class_="prdct-desc-cntnr-name hasRatings")
        discounted_prices = soup.find_all("div", class_="prc-box-dscntd")

        products = []
        for name, price in zip(product_names, discounted_prices):
            product_name = name.get_text(strip=True)
            product_price = price.get_text(strip=True)
            products.append((product_name, product_price))

        # DataFrame
        df_products = pd.DataFrame(products, columns=["Product Name", "Discounted Price"])

        # Clean and convert prices
        def clean_price(price_str):
            # Remove currency symbols and extra characters
            price_str = price_str.replace('₺', '').replace(',', '.').strip()
            try:
                return float(price_str)
            except ValueError:
                return None

        df_products["Discounted Price"] = df_products["Discounted Price"].apply(clean_price)

        # Drop rows where conversion failed
        df_products = df_products.dropna(subset=["Discounted Price"])

        # Sort by price
        df_products = df_products.sort_values(by="Discounted Price")
        df_products.reset_index(drop=True, inplace=True)

        # Convert DataFrame to HTML
        tables = [df_products.to_html(classes='data', header="true")]

        return render_template('index.html', tables=tables, search=search)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
