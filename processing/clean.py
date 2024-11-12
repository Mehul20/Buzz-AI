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
            "Professors": professor_names,
            "Campus Index": raw_sections[curr_section][4]
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

def special_topics_design(clean_data_model):
    special_topics_classes = {"CX 4803", "CS 4803", "CS 8803", "CSE 4803", "CSE 8803", "ECE 8803", "ECE 4803"}
    new_entries = {}
    for key in clean_data_model.keys():
        if key in special_topics_classes:
            all_section_info = clean_data_model[key]["Section Information"]
            for section in all_section_info.keys(): 
                new_entries[key + "-" + section] = {
                    "Name": "",
                    "Description": "",
                    "Section Information": {
                        section: all_section_info[section]
                    }
                }
    for sp_class in special_topics_classes:
        if sp_class in clean_data_model.keys():
            del clean_data_model[sp_class]
    clean_data_model = clean_data_model | new_entries
    return clean_data_model

if __name__ == "__main__":
    filePath = "../DataSource/data.json"
    data = read_data(filePath)
    relevant_courses = clean_data_relevant_courses(data)
    clean_data_model = create_data_model(relevant_courses)
    clean_data_model = special_topics_design(clean_data_model)

    with open("data_clean.json", "w") as json_file:
        json.dump(clean_data_model, json_file, indent=4)