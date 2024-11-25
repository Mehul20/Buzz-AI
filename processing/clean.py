import json
from special_title import getTitle
from professor_bio import get_professor_description

def read_data(filePath):
    with open(filePath, 'r') as file:
        data = json.load(file)
    return data

def extract_courses(data):
    return data["courses"]

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
            "Campus Index": raw_sections[curr_section][4],
            "CRN": raw_sections[curr_section][0],
            "Research Area": ""
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
            "Section Information": course_sections,
            "Syllabus": ""
        }
    return clean_data_model

def clean_professor_name_format(prof):
    splitted = prof.split(" ")
    name = splitted[0] + "-" + splitted[1]
    return name

def compute_research_area(course_subject, curr_professors):
    compatible_courses = {"CS", "CSE", "CM", "CX"}
    all_prof_research_areas = ""
    if course_subject in compatible_courses:
        for prof in curr_professors:
            prof = clean_professor_name_format(prof)
            professor_research_area = get_professor_description(prof)
            if len(professor_research_area) > 0:
                if len(all_prof_research_areas) > 0:
                    all_prof_research_areas = all_prof_research_areas + "Another Professor - " + professor_research_area
                else:
                    all_prof_research_areas = professor_research_area
    return all_prof_research_areas

def special_topics_design(clean_data_model):
    special_topics_classes = []
    new_entries = {}

    for key in clean_data_model.keys():
        course_number_isolate = key.split(" ")[1]
        course_subject = key.split(" ")[0]

        if course_number_isolate == "4803" or course_number_isolate == "8803":
            all_section_info = clean_data_model[key]["Section Information"]
            for section in all_section_info.keys(): 
                curr_CRN = all_section_info[section]["CRN"]
                get_name = getTitle(curr_CRN)
                curr_professors = all_section_info[section]["Professors"]
                all_prof_research_areas = compute_research_area(course_subject, curr_professors)
                all_section_info[section]["Research Area"] = all_prof_research_areas

                new_entries[key + "-" + section] = {
                    "Name": get_name,
                    "Description": "",
                    "Section Information": {
                        section: all_section_info[section]
                    },
                    "Syllabus" : ""
                }
            special_topics_classes.append(key)
    
    for sp_class in special_topics_classes:
        if sp_class in clean_data_model.keys():
            del clean_data_model[sp_class]
    
    clean_data_model = clean_data_model | new_entries
    return clean_data_model

def manual_data_merging(clean_data_model):
    manual_data = read_data("manual_inputs.json")
    for key in manual_data.keys():
        if key in clean_data_model.keys():
            if "Name" in manual_data[key].keys():
                clean_data_model[key]["Name"] = manual_data[key]["Name"]
            if "Description" in manual_data[key].keys():
                clean_data_model[key]["Description"] = manual_data[key]["Description"]
            if "Syllabus" in manual_data[key].keys():
                clean_data_model[key]["Syllabus"]  = manual_data[key]["Syllabus"]
    return clean_data_model

def delete_irrelevant_classes(clean_data_model):
    doctoral_thesis = []
    for key in clean_data_model.keys():
        if key.split(" ")[1] == "9000":
            doctoral_thesis.append(key)
    
    for curr_class in doctoral_thesis:
        del clean_data_model[curr_class]

    return clean_data_model

if __name__ == "__main__":
    filePath = "../DataSource/data.json"
    data = read_data(filePath)
    relevant_courses = extract_courses(data)
    clean_data_model = create_data_model(relevant_courses)
    clean_data_model = special_topics_design(clean_data_model)
    clean_data_model = manual_data_merging(clean_data_model)
    clean_data_model = delete_irrelevant_classes(clean_data_model)

    with open("data_clean.json", "w") as json_file:
        json.dump(clean_data_model, json_file, indent=4)