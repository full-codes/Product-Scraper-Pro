import requests
from bs4 import BeautifulSoup
import csv
import time

# Category page URL (modify according to the website)
category_url = 'https://example.com/category/your-category'

headers = {'User-Agent': 'Mozilla/5.0'}

# List to store product data
products = []

# Function to gather product links from a category page
def get_product_links(page_url):
    response = requests.get(page_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Replace 'product-link' with the correct class or element
        links = soup.find_all('a', class_='product-link')
        product_links = ['https://example.com' + link['href'] for link in links]
        return product_links
    else:
        print(f"Failed to access page: {page_url}")
        return []

# Function to gather product details
def get_product_details(product_url):
    response = requests.get(product_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Replace these selectors according to the website's structure
        name = soup.find('h1', class_='product-title').get_text(strip=True)
        price = soup.find('span', class_='price').get_text(strip=True)
        description = soup.find('div', class_='product-description').get_text(strip=True)
        return {'name': name, 'price': price, 'description': description}
    else:
        print(f"Failed to access product: {product_url}")
        return None

# Collect product links from multiple pages
for page in range(1, 6):  # For example, 5 pages
    page_url = f"{category_url}?page={page}"
    links = get_product_links(page_url)
    for link in links:
        product_data = get_product_details(link)
        if product_data:
            products.append(product_data)
        time.sleep(1)  # Pause to avoid being blocked by the website

# Save data to CSV file
with open('products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['name', 'price', 'description'])
    writer.writeheader()
    for product in products:
        writer.writerow(product)

print('Data collection complete. Saved to products.csv')
