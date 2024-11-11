import json

def read_data(filePath):
    with open(filePath, 'r') as file:
        data = json.load(file)
    return data

def clean_data_relevant_courses(data):
    subjects_requried = {"CX", "CSE", "CS", "ECE", "CM"}
    relevant_courses = {}
    courses = data["courses"]
    for key in courses.keys():
        subject = key.split(" ")
        if subject[0] in subjects_requried:
            relevant_courses[key] = courses[key]
    return relevant_courses

def extract_sections(raw_sections):
    course_sections = {}
    for curr_section in raw_sections.keys():
        section_name = curr_section
        try:
            professor_names = raw_sections[curr_section][1][0][4]
        except:
            professor_names = []
        course_sections[section_name] = {
            "Professors": professor_names
        }
    return course_sections

def create_data_model(relevant_courses):
    clean_data_model = {}
    for key in relevant_courses.keys():
        course_information = relevant_courses[key]
        
        course_name = course_information[0]
        course_description = course_information[-1]
        
        raw_sections = course_information[1]
        course_sections = extract_sections(raw_sections)

        clean_data_model[key] = {
            "Name": course_name,
            "Description": course_description,
            "Section Information": course_sections
        }
    return clean_data_model


filePath = "data.json"
data = read_data(filePath)
relevant_courses = clean_data_relevant_courses(data)
clean_data_model = create_data_model(relevant_courses)
print(clean_data_model)

with open("data_clean.json", "w") as json_file:
    json.dump(clean_data_model, json_file, indent=4)