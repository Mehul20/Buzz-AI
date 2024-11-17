import requests
from bs4 import BeautifulSoup

def get_professor_description(professor_name):
    url = "https://www.cc.gatech.edu/people/" + professor_name
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    biography_section = soup.find('h2', string='Biography')
    if biography_section:
        biography = biography_section.find_next('p').text.strip()
        return biography
    
    return ""