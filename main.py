import os
import re
import csv
import fitz
import json

def extract_name_by_font(doc):
    page = doc[0]
    text_dict = page.get_text("dict")
    max_font_size = 0
    candidate_name = ""

    for b in text_dict.get("blocks", []):
        if "lines" in b:
            for l in b["lines"]:
                for s in l["spans"]:
                    text = s["text"].strip()
                    font_size = s["size"]
                    if font_size > max_font_size and len(text) > 2:
                        if text.upper() not in ["EXPERIENCE", "EDUCATION", "SKILLS", "RESUME", "CV", "CURRICULUM VITAE"]:
                            max_font_size = font_size
                            candidate_name = text
    return candidate_name

def extract_section(text, target_heading):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    standard_headings = [
        "EDUCATION", "SKILLS", "EXPERIENCE", "WORK EXPERIENCE", 
        "PROFESSIONAL EXPERIENCE", "EMPLOYMENT HISTORY", 
        "PROJECTS", "CERTIFICATIONS", "ABOUT ME", "ACHIEVEMENTS"
    ]
    is_in_target_section = False
    extracted_data = []

    for line in lines:
        clean_line = line.upper()
        if any(heading == clean_line for heading in standard_headings):
            if clean_line == target_heading.upper():
                is_in_target_section = True
                continue
            elif is_in_target_section:
                break
        if is_in_target_section:
            extracted_data.append(line)
    return extracted_data

def build_final_json(name, email, phone, skills, projects):
    resume_data = {
        "candidate_info": {
            "name": name,
            "contact": {
                "email": email[0] if email else None,
                "phone": phone[0] if phone else None
            }
        },
        "technical_stack": {"skills": skills},
        "projects_portfolio": []
    }

    current_project = None
    for line in projects:
        if len(line) < 100 and not line.startswith(('-', '•', '*', '🔹')):
            if current_project:
                resume_data["projects_portfolio"].append(current_project)
            current_project = {"title": line, "details": []}
        elif current_project:
            current_project["details"].append(line.strip('- •*🔹').strip())
            
    if current_project:
        resume_data["projects_portfolio"].append(current_project)

    return resume_data

def process_single_resume(pdf_path):
    doc = fitz.open(pdf_path)
    
    full_text_sorted = ""
    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: b[1])
        full_text_sorted += "\n".join([b[4] for b in blocks]) + "\n"

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails_found = re.findall(email_pattern, full_text_sorted)

    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\d{10}'
    phone_nums_found = re.findall(phone_pattern, full_text_sorted)

    name = extract_name_by_font(doc)
    if name and name.count(' ') > len(name) / 3:
        name = name.replace(" ", "")

    my_skills = extract_section(full_text_sorted, "SKILLS")
    
    my_projects = extract_section(full_text_sorted, "PROJECTS")
    if not my_projects:
        my_projects = extract_section(full_text_sorted, "EXPERIENCE")
    if not my_projects:
        my_projects = extract_section(full_text_sorted, "WORK EXPERIENCE")
    if not my_projects:
        my_projects = extract_section(full_text_sorted, "PROFESSIONAL EXPERIENCE")

    return build_final_json(name, emails_found, phone_nums_found, my_skills, my_projects)

def run_batch_processor(folder_path):
    print(f"🔍 Scanning folder: '{folder_path}'...\n")
    all_parsed_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"): 
            file_path = os.path.join(folder_path, filename)
            print(f"⚙️ Processing: {filename}")
            
            parsed_resume = process_single_resume(file_path)
            all_parsed_data.append(parsed_resume)

    with open("all_parsed_resumes.json", "w", encoding="utf-8") as f:
        json.dump(all_parsed_data, f, indent=4)
        
    print(f"\n{len(all_parsed_data)} resumes successfully parsed into 'all_parsed_resumes.json'")

def export_to_csv(json_file_path, csv_file_path):
    print(f"\nConverting {json_file_path} to Excel format...")
    
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    headers = ["Candidate Name", "Email", "Phone", "Top Skills", "Projects Portfolio"]

    with open(csv_file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers) 

        for candidate in data:
            name = candidate.get("candidate_info", {}).get("name", "N/A")
            email = candidate.get("candidate_info", {}).get("contact", {}).get("email") or "N/A"
            phone = candidate.get("candidate_info", {}).get("contact", {}).get("phone") or "N/A"

            skills_list = candidate.get("technical_stack", {}).get("skills", [])
            skills_str = ", ".join(skills_list) 

            projects_list = candidate.get("projects_portfolio", [])
            projects_str = ""
            for p in projects_list:
                projects_str += f"[{p.get('title', '')}] "

            writer.writerow([name, email, phone, skills_str, projects_str])

    print(f"Success! Excel sheet ready at '{csv_file_path}'")

if __name__ == "__main__":
    resume_folder = "resumes" 
    
    if not os.path.exists(resume_folder):
        os.makedirs(resume_folder)
        print(f"A '{resume_folder}' folder has been created. Put some resumes in it and run again!")
    else:
        run_batch_processor(resume_folder)
        export_to_csv("all_parsed_resumes.json", "candidates_database.csv")