import requests
import re
import json

def get_page_data(url, output_file):

    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def parse_content(f_path, json_path):

    with open(f_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    title_pattern = re.compile(r'<p class="courseblocktitle"><strong>(.*?)</strong></p>', re.DOTALL)
    desc_pattern = re.compile(r'<p class="courseblockdesc">(.*?)</p>', re.DOTALL)

    titles = title_pattern.findall(html_content)
    descriptions = desc_pattern.findall(html_content)
    courses_dict = {}

    for i in range(len(titles)):
        courses_dict[i + 1] = {
            "title": titles[i].split('.'),
            "description": descriptions[i].strip().split('.')
        }
   
    courses_list = list(courses_dict.values())
    
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(courses_list, json_file, ensure_ascii=False, indent=4)
    print(f"All courses have been successfully saved to {json_path}")

if __name__ == "__main__":
    html_f_path = "cs_courses.html"
    courses_url = "https://catalog.gatech.edu/coursesaz/cs/"
    file_name = "cs_courses.html"
    output_json_path = 'courses_data.json'
    get_page_data(url=courses_url, output_file=file_name)
    parse_content(html_f_path, output_json_path)