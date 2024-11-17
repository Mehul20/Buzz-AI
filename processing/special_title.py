import requests
from bs4 import BeautifulSoup

def getTitle(CRN):
    url = "https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=202502&crn_in=" + str(CRN)

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='datadisplaytable')

        if table:
            cell = table.find('td', class_='dddefault')
            if cell:
                long_title_span = cell.find('span', string='Long Title: ')
                if long_title_span:
                    long_title = long_title_span.next_sibling.strip()
                    return long_title
    return ""
