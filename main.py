import csv
from bs4 import BeautifulSoup
import requests


def scrape_and_write_data(url, writer):
  """
  Scrapes product data (title, price, and category) from a given URL and writes it to a CSV writer object.

  Args:
      url (str): The URL of the product collection page.
      writer (csv.writer): The CSV writer object for the output file.
  """

  # Send a GET request and get the HTML content
  response = requests.get(url)

  # Check for successful response
  if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all product blocks
    product_blocks = soup.find_all('div', class_='product-block__title-price')

    # Extract collection name from the URL for category
    category = url.split("/")[-1]

    # Extract data from each product block and write to CSV
    for block in product_blocks:
      # Get the title
      title_element = block.find('a', class_='title')
      title = title_element.text.strip() if title_element else ""

      # Get the price
      price_element = block.find('span', class_='amount')
      price = price_element.text.strip() if price_element else ""

      # Write data as a row with category
      writer.writerow([category, title, price])

    print(f"Data for collection '{category}' scraped successfully.")
  else:
    print(f"Failed to retrieve data from {url}")


# Define output filename
filename = "all_products_data.csv"

# Open the CSV file in append mode with UTF-8 encoding (outside the loop)
with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
  # Create a CSV writer object
  writer = csv.writer(csvfile)

  # Write the header row for title, price, and category (only once, before the loop)
  writer.writerow(["Category", "Title", "Price"])

  # Define URLs for product collections
  urls = [
      "https://the-barn-biomarket.myshopify.com/en/collections/viandes",
      "https://the-barn-biomarket.myshopify.com/en/collections/fruits",
      "https://the-barn-biomarket.myshopify.com/en/collections/cremerie-1",
      "https://the-barn-biomarket.myshopify.com/en/collections/legumes",
      "https://the-barn-biomarket.myshopify.com/en/collections/boulangerie",
      "https://the-barn-biomarket.myshopify.com/en/collections/boissons",
      "https://the-barn-biomarket.myshopify.com/en/collections/epicerie",
      "https://the-barn-biomarket.myshopify.com/en/collections/glutenfree",
      "https://the-barn-biomarket.myshopify.com/en/collections/vegetarien-vegan",
      "https://the-barn-biomarket.myshopify.com/en/collections/apero",
      "https://the-barn-biomarket.myshopify.com/en/collections/petit-dejeuner",
      "https://the-barn-biomarket.myshopify.com/en/collections/gamme-zero-dechets",
      "https://the-barn-biomarket.myshopify.com/en/collections/maison-et-hygiene",
  ]

  # Loop through each URL and call the scrape_and_write_data function
  for url in urls:
    scrape_and_write_data(url, writer)

  print(f"All data scraped and written to {filename}")
