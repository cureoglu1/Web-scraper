import requests
from bs4 import BeautifulSoup
import pandas as pd

# Defining URL is for the search query
url = "https://www.trendyol.com/sr?q=iphone"

# Send a GET request
response = requests.get(url)
html_content = response.content

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Defining product names' path and prices
product_names = soup.find_all("span", attrs={"class": "prdct-desc-cntnr-name hasRatings"})
discounted_prices = soup.find_all("div", attrs={"class": "prc-box-dscntd"})

# Initializing a list
products = []

# Iterate through the extracted names and prices
for name, price in zip(product_names, discounted_prices):
    product_name = name.get_text(strip=True)  
    product_price = price.get_text(strip=True)
    products.append((product_name, product_price))

# DataFrame
df_products = pd.DataFrame(products, columns=["Product Name", "Discounted Price"])

# Sort by price and reset index no.
df_products = df_products.sort_values(by="Discounted Price")
df_products.reset_index(drop=True, inplace=True)

# Output of DF
print(df_products)
