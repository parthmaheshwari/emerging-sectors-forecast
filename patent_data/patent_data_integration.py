import os
import json
from lxml import etree
from tqdm import tqdm

# Set the working directory
os.chdir('fullpatentdata')

# Function to extract patent data from XML root
def extract_patent_data(root):
    data = {}

    # Basic patent information
    data['patent_id'] = root.get('id')
    data['date_produced'] = root.get('date-produced')
    data['date_published'] = root.get('date-publ')
    data['country'] = root.get('country')

    # Publication Reference
    pub_ref = root.find('.//publication-reference/document-id')
    if pub_ref is not None:
        data['publication_reference'] = {
            "doc_number": pub_ref.find('doc-number').text,
            "date": pub_ref.find('date').text,
            "country": pub_ref.find('country').text,
            "id": pub_ref.get('id')
        }

    # Application Reference
    app_ref = root.find('.//application-reference/document-id')
    if app_ref is not None:
        data['application_reference'] = {
            "doc_number": app_ref.find('doc-number').text,
            "date": app_ref.find('date').text,
            "country": app_ref.find('country').text,
            "id": app_ref.get('id')
        }

    # US Term of Grant
    us_term_of_grant = root.find('.//us-term-of-grant/us-term-extension')
    data['us-term-of-grant'] = us_term_of_grant.text if us_term_of_grant is not None else "Not Found"

    # IPCR Classifications
    data['classifications-ipcr'] = [{
        "classification_level": el.find('classification-level').text,
        "section": el.find('section').text,
        "class": el.find('class').text,
        "subclass": el.find('subclass').text,
        "main_group": el.find('main-group').text,
        "subgroup": el.find('subgroup').text
    } for el in root.findall('.//classification-ipcr')]

    # CPC Classifications
    data['classifications-cpc'] = [{
        "section": el.find('section').text,
        "class": el.find('class').text,
        "subclass": el.find('subclass').text,
        "main_group": el.find('main-group').text,
        "subgroup": el.find('subgroup').text
    } for el in root.findall('.//classification-cpc')]

    # Invention Title
    invention_title = root.find('.//invention-title')
    data['invention-title'] = invention_title.text if invention_title is not None else "Not Found"

    # US Field of Classification Search
    data['us-field-of-classification-search'] = [el.text.strip() for el in root.findall('.//us-field-of-classification-search/classification-national/main-classification') if el.text]

    
    
    # US citations
    citation_elements = root.findall('.//us-citation')
    citations = []
    for citation_element in citation_elements:
        doc_number = citation_element.find('.//doc-number').text if citation_element.find('.//doc-number') is not None else None
        kind = citation_element.find('.//kind').text if citation_element.find('.//kind') is not None else None
        name = citation_element.find('.//name').text if citation_element.find('.//name') is not None else None
        date = citation_element.find('.//date').text if citation_element.find('.//date') is not None else None
        category = citation_element.find('.//category').text if citation_element.find('.//category') is not None else None

        othercit = citation_element.find('.//othercit')
        othercit_text = othercit.text if othercit is not None else None

        citation_data = {
            "doc_number": doc_number,
            "kind": kind,
            "name": name,
            "date": date,
            "category": category,
            "othercit": othercit_text
        }
        citations.append(citation_data)

    data['us-citations'] = citations
    
    # Applicant data
    us_applicants_data = []

    us_applicant_elements = root.findall('.//us-applicant')

    for applicant in us_applicant_elements:
        org_name_element = applicant.find('.//addressbook/orgname')
        org_name = org_name_element.text if org_name_element is not None else "Not Found"

        address_element = applicant.find('.//addressbook/address')
        city = address_element.find('city').text if address_element is not None and address_element.find('city') is not None else "Not Found"
        state = address_element.find('state').text if address_element is not None and address_element.find('state') is not None else "Not Found"
        country = address_element.find('country').text if address_element is not None and address_element.find('country') is not None else "Not Found"
        address = f"{city}, {state}, {country}" if city != "Not Found" or state != "Not Found" or country != "Not Found" else "Not Found"

        us_applicants_data.append({
            "orgname": org_name,
            "address": address
        })

    data['us-applicants'] = us_applicants_data
    
    # Inventors
    data['inventors'] = []
    for el in root.findall('.//inventor'):
        first_name = el.find('.//first-name')
        last_name = el.find('.//last-name')
        city_el = el.find('.//address/city')
        state_el = el.find('.//address/state')
        country_el = el.find('.//address/country')

        name = f"{first_name.text if first_name is not None else 'Not Found'} {last_name.text if last_name is not None else 'Not Found'}"
        address = f"{city_el.text if city_el is not None else 'Not Found'}, {state_el.text if state_el is not None else 'Not Found'}, {country_el.text if country_el is not None else 'Not Found'}"

        data['inventors'].append({"name": name, "address": address})

    
    
    # Agents
    
    data['agents'] = []
    for el in root.findall('.//agent'):
        orgname_el = el.find('.//orgname')
        first_name_el = el.find('.//first-name')
        last_name_el = el.find('.//last-name')
        country_el = el.find('.//country')

        if orgname_el is not None:
            name = orgname_el.text
        elif first_name_el is not None and last_name_el is not None:
            name = f"{first_name_el.text} {last_name_el.text}"
        else:
            name = "Not Found"

        country = country_el.text if country_el is not None else "Not Found"

        agent_data = {
            "name": name,
            "country": country
        }
        data['agents'].append(agent_data)
    
    
    # Assignees
    data['assignees'] = []
    for el in root.findall('.//assignee'):
        orgname_element = el.find('.//orgname')
        orgname = orgname_element.text if orgname_element is not None else "Not Found"

        address_element = el.find('.//address')
        if address_element is not None:
            city_element = address_element.find('city')
            state_element = address_element.find('state')
            country_element = address_element.find('country')

            city = city_element.text if city_element is not None else "Not Found"
            state = state_element.text if state_element is not None else "Not Found"
            country = country_element.text if country_element is not None else "Not Found"

            address = f"{city}, {state}, {country}"
        else:
            address = "Address Not Found"

        assignee_data = {
            "orgname": orgname,
            "address": address
        }
        
        data['assignees'].append(assignee_data)
    
       # Primary Examiner Data
    primary_examiner = root.find('.//primary-examiner')
    if primary_examiner is not None:
        last_name_element = primary_examiner.find('last-name')
        first_name_element = primary_examiner.find('first-name')
        department_element = primary_examiner.find('department')

        last_name = last_name_element.text if last_name_element is not None else "Not Found"
        first_name = first_name_element.text if first_name_element is not None else "Not Found"
        department = department_element.text if department_element is not None else "Not Found"

        examiner_data = {
            "last_name": last_name,
            "first_name": first_name,
            "department": department
        }
    else:
        examiner_data = {"last_name": "Not Found", "first_name": "Not Found", "department": "Not Found"}
    
    data['examiner'] = examiner_data

    # Abstract
    abstract = root.find('.//abstract/p')
    data['abstract'] = abstract.text if abstract is not None else "Abstract not found"

    return data


# Function to split XML documents in a file
def split_xml_documents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = ''
        for line in file:
            if line.strip().startswith('<?xml'):
                if xml_content:
                    yield xml_content
                    xml_content = ''
                xml_content = line  
            else:
                xml_content += line
        if xml_content.strip():  
            yield xml_content

# Load filenames from a JSON file
directory_path='fullpatentdata'
filenames=os.listdir()

# Process a subset of files and extract patent data
patent_data_list= []
for filename in tqdm(filenames):
    if filename.endswith('.xml'):  
        file_path = os.path.join(directory_path, filename)
        xml_documents = split_xml_documents(file_path)
        for xml_content in xml_documents:
            try:
                root = etree.fromstring(xml_content.encode('utf-8'))
                patent_data = extract_patent_data(root)
                patent_data_list.append(patent_data)
            except etree.XMLSyntaxError as e:
                print(f"Error parsing XML content in file {filename}: {e}")

# Write extracted data to a JSONL file
jsonl_file_path = 'patent_data_list_xmls.jsonl'
with open(jsonl_file_path, 'w', encoding='utf-8') as f:
    for patent_data in patent_data_list:
        json.dump(patent_data, f, ensure_ascii=False)
        f.write("\n")
