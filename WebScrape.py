from bs4 import BeautifulSoup

import requests


class WebScraper:

  def __init__(self, url):
    self.url = url

  def scrape_visible_text(self):
    # Send a GET request to the URL
    response = requests.get(self.url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
      # Parse the HTML content using BeautifulSoup
      soup = BeautifulSoup(response.text, 'html.parser')

      # Define elements to extract text and attributes
      elements_with_text = [
          'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong', 'em', 'mark',
          'small', 'del', 'ins', 'sub', 'sup', 'span'
      ]
      elements_with_attributes = {'a': 'href', 'img': 'src'}

      # Concatenate visible text
      visible_texts = []
      for element in soup.find_all(elements_with_text +
                                   list(elements_with_attributes.keys())):
        tag_name = element.name
        if tag_name in elements_with_text:
          text_content = element.get_text(separator=' ', strip=True)
          visible_texts.append(f"'{tag_name}:{text_content}'")
        elif tag_name in elements_with_attributes:
          attribute_name = elements_with_attributes[tag_name]
          attribute_value = element.get(attribute_name)
          text_content = element.get_text(separator=' ', strip=True)
          visible_texts.append(
              f"'{tag_name}:{attribute_name}={attribute_value} {text_content}'"
          )

      result_text = ' '.join(visible_texts)

      # Remove <a> elements if character count is greater than 10,000
      if len(result_text) > 10000:
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a'):
          a_tag.decompose()  # Remove <a> elements

        result_text = ' '.join([
            f"'{tag.name}:{tag.get_text(separator=' ', strip=True)}'"
            for tag in soup.find_all(elements_with_text)
        ])

        # If still over 10,000 characters, remove elements with attributes
        if len(result_text) > 10000:
          for tag_name in elements_with_attributes:
            for tag in soup.find_all(tag_name):
              tag.decompose()

          result_text = ' '.join([
              f"'{tag.name}:{tag.get_text(separator=' ', strip=True)}'"
              for tag in soup.find_all(elements_with_text)
          ])

      return result_text

    elif response.status_code >= 500:
      return f"Failed. Status code: {response.status_code}"
    else:
      return f"Error: Failed to get content."


# Example usage
# user_url = input("Enter the URL to scrape: ")
# web_scraper = WebScraper(user_url)
# result = web_scraper.scrape_visible_text()
# print(result)