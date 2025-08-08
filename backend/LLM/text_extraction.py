from groq import Groq
from typing import Dict, Any
import base64
import io
from PIL import Image
import re

def extract_resume_text_with_groq_for_ml(base64_image: str) -> Dict[str, Any]:
    
    client = Groq(api_key="put your api key")
    model = "meta-llama/llama-4-scout-17b-16e-instruct"
    
    try:
        if not base64_image:
            return {"success": False, "error": "No image data provided"}
        
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
        
        try:
            image_data = base64.b64decode(base64_image)
            Image.open(io.BytesIO(image_data))  # Just to validate
        except Exception as img_error:
            return {"success": False, "error": f"Invalid image data: {str(img_error)}"}

        # Modified system prompt for better extraction
        system_prompt = """
        You are an expert resume analyzer. Extract only the professional content that's relevant for job category classification.
        Focus on: skills, technologies, job roles, experience descriptions, achievements, and qualifications.
        Ignore: personal contact information, formatting, dates, company locations.
        """
        
        user_prompt = """
        Extract the professional content from this resume image for job category classification:
        - Job titles and roles
        - Technical skills and technologies
        - Experience descriptions (what they did, achieved)
        - Professional summary/objective
        - Relevant qualifications and certifications
        
        Do NOT include: names, emails, phone numbers, addresses, LinkedIn profiles, company locations, specific dates.
        Return clean, relevant professional text only.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=3000,
            temperature=0.1
        )

        raw_text = response.choices[0].message.content
        
        #text cleaning
        cleaned_text = clean_for_ml_model(raw_text)
        
        return {
            "success": True,
            "raw_extracted_text": raw_text,  
            "ml_ready_text": cleaned_text,    
            "message": "Resume text extracted and cleaned for ML model"
        }

    except Exception as e:
        return {"success": False, "error": f"Text extraction failed: {str(e)}"}

def clean_for_ml_model(text: str) -> str:
    """
    Clean extracted resume text specifically for ML model input
    """
    if not text:
        return ""
    
    
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)  
    text = re.sub(r'linkedin\.com/in/[^\s]+', '', text)  
    text = re.sub(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '', text)  
    text = re.sub(r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln)\b[^,\n]*', '', text)  
    
    # Remove section headers and labels that add noise
    text = re.sub(r'^(Name|Phone|Email|LinkedIn|Address):\s*[^\n]*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^(Summary|Experience|Skills|Education|Certifications/Awards):\s*\n?', '', text, flags=re.MULTILINE)
    
    # Remove dates and time periods
    text = re.sub(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\s*[-–]\s*(?:Present|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b', '', text)
    text = re.sub(r'\b\d{1,2}/\d{4}\s*[-–]\s*(?:Present|\d{1,2}/\d{4})\b', '', text)
    text = re.sub(r'\b\d{4}\s*[-–]\s*(?:Present|\d{4})\b', '', text)
    
    # Remove company locations
    text = re.sub(r',\s*[A-Za-z\s]+,\s*[A-Z]{2}(?:\s|$)', ' ', text)
    text = re.sub(r',\s*Remote(?:\s|$)', ' ', text)
    
    # Clean formatting
    text = re.sub(r'\*+', '', text)  # Remove asterisks
    text = re.sub(r'#+\s*', '', text)  # Remove hash marks
    text = re.sub(r'[•\-\*]\s*', '', text)  # Remove bullet points
    text = re.sub(r'\n+', ' ', text)  # Replace newlines with spaces
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
    
    # Extract and preserve key professional terms
    # This helps the model focus on relevant content
    professional_terms = []
    
    # Extract years of experience
    exp_years = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?experience', text, re.IGNORECASE)
    if exp_years:
        professional_terms.append(f"{max(exp_years)} years experience")
    
    # Extract common tech keywords
    tech_keywords = r'\b(?:JavaScript|Python|Java|React|Angular|Vue|Node\.js|HTML|CSS|SQL|MongoDB|PostgreSQL|AWS|Docker|Kubernetes|Git|Agile|Scrum|Machine Learning|AI|Data Science|Frontend|Backend|Full Stack|DevOps|Cloud|API|REST|GraphQL|TypeScript|C\+\+|C#|PHP|Ruby|Django|Flask|Spring|Express|TailwindCSS|Bootstrap|Figma|Adobe|Photoshop|Selenium|Jest|Testing|CI/CD|Linux|Windows|Azure|GCP|Android|iOS|Swift|Kotlin|Flutter|Dart|Tableau|PowerBI|Excel|Pandas|NumPy|TensorFlow|PyTorch|Scikit|R|Stata|SPSS|Salesforce|SAP|Oracle|MySQL|NoSQL|Redis|ElasticSearch|Kafka|Spark|Hadoop|Blockchain|Ethereum|Solidity)\b'
    tech_matches = re.findall(tech_keywords, text, re.IGNORECASE)
    if tech_matches:
        professional_terms.extend(set([t.lower() for t in tech_matches]))
    
    # Extract job roles/titles
    role_keywords = r'\b(?:Developer|Engineer|Analyst|Manager|Designer|Architect|Lead|Senior|Junior|Specialist|Consultant|Director|Coordinator|Administrator|Scientist|Researcher|Technician|Officer|Associate|Assistant|Intern)\b'
    role_matches = re.findall(role_keywords, text, re.IGNORECASE)
    if role_matches:
        professional_terms.extend(set([r.lower() for r in role_matches]))
    
    # Clean the main text and combine with extracted terms
    cleaned_main = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)  # Keep only alphanumeric and spaces
    cleaned_main = re.sub(r'\s+', ' ', cleaned_main).strip().lower()
    
    # Combine professional terms with cleaned text
    final_text = ' '.join(professional_terms) + ' ' + cleaned_main
    final_text = re.sub(r'\s+', ' ', final_text).strip()
    
    return final_text

