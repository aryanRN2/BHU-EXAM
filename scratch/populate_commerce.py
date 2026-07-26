import json
import os
import re

MAPPING_DICTIONARY = {
    # Semester 1
    "BCF-111": "COMMJ52", # Business Environment (old FMM) -> COMMJ52 (Business Environment)
    "BCF-112": "COMFMJ32 / COMMJ53", # Business Laws -> Business Law
    "BCF-113": "COMMN11 / COMFMN11", # Business Economics -> Business Economics
    "BCF-114": "COMMD22 / COMFMN21", # Business Organisation -> Business Organisation
    "BCF-115": "COMFSE11", # Business Communication
    "BCF-116": "COMMN41 / COMFMN41", # Business Statistics -> Business Statistics
    "BCH-111": "COMMJ11 / COMFMJ11", # Financial Accounting - I -> Financial Accounting
    "BCH-112": "COMMN21 / COMFMN21", # Principles of Management -> Business Management / Business Organisation & Management
    "BCH-113": "COMMJ52", # Business Environment
    "BCH-114": "COMSE21 / COMFSE21", # Monetary Theory
    "BCH-115": "COMMJ31 / COMFMJ43", # Fundamentals of Marketing -> Fundamentals of Marketing
    "BCH-E111": "BCHE111", # English Language
    
    # Semester 2
    "BCF-121": "COMMN21 / COMFMN21", # Fundamentals of Business Management -> Business Management
    "BCF-122": "COMFMJ21 / COMMJ21", # Fundamentals of Business Finance -> Business Finance
    "BCF-123": "COMMD21 / COMMJ11", # Fundamental of Accounting -> Basic Accounting / Financial Accounting
    "BCF-124": "COMMJ31 / COMFMJ43", # Fundamentals of Marketing -> Fundamentals of Marketing
    "BCF-125": "COMFSE21 / COMMJ82", # Fundamentals of Banking -> Monetary Theory & Banking / Banking Laws and Insurance
    "BCF-126": "COMMJ82", # Fundamentals of Insurance -> Banking Laws and Insurance
    "BCH-121": "COMMD22 / COMFMN21", # Business Organisation
    "BCH-122": "COMMJ11 / COMFMJ11", # Financial Accounting - II
    "BCH-123": "COMFSE21 / COMMJ82", # Banking and Financial Institutions
    "BCH-124": "COMSE11 / COMFSE31", # Business Entrepreneurship
    "BCH-125": "COMMJ32 / COMFMJ44", # Fundamentals of HRM
    "BCH-126": "COMFSE11 / COMFMV31", # IT & Business Communication
    
    # Semester 3
    "BCF-211": "COMFMJ31 / COMMV31", # Corporate Accounting -> Specialised Accounting / Specialised Account
    "BCF-212": "COMFMJ42 / COMMJ42", # Corporate Financial Management -> Financial Management
    "BCF-213": "COMFMV61 / COMMV61", # Corporate Taxation -> GST and Customs Duty
    "BCF-214": "COMSE32 / COMFMJ53", # Corporate Auditing -> Auditing
    "BCF-215": "COMMJ62", # Corporate Laws -> Company Law & Secretarial Practices
    "BCF-216": "COMMJ63 / COMFMJ83", # Corporate Governance -> Business Ethics and Governance
    "BCH-211": "COMFMJ32 / COMMJ53", # Business Regulatory Framework - I -> Business Law
    "BCH-212": "COMMN11 / COMFMN11", # Business Economics - I
    "BCH-213": "COMFMJ31 / COMMV31", # Specialised Accounts - I -> Specialised Accounting
    "BCH-214": "COMFMJ41 / COMMJE54", # Cost Accounting - I
    "BCH-215": "COMFMJ21 / COMMJ21", # Fundamentals of Business Finance
    "BCH-216": "COMMN41 / COMFMN41", # Basic Statistics -> Business Statistics
    
    # Semester 4
    "BCF-221": "COMFMJ52 / COMMJE55", # Indian Financial System -> Financial Markets & Institutions
    "BCF-222": "COMFMJ61 / COMMJ61", # Financial Analysis
    "BCF-223": "COMFMJ54 / COMMJE65", # Fee Based Financial Services -> Financial Services
    "BCF-224": "COMFMV31 / COMMV31", # Computer Applications in Financial Markets -> Accounting with IT Tools / Specialised Account
    "BCF-225": "COMSE31 / COMFSE22", # Indian Fiscal Management -> Public Finance
    "BCF-226": "COMMJE75 / COMFMJ81", # Financial Market Regulations -> Risk Management / Derivatives
    "BCF-299": "COMFMJ61 / COMMJ61", # Financial Analysis
    "BCH-221": "COMFMJ32 / COMMJ53", # Business Regulatory Framework-II -> Business Law
    "BCH-222": "COMMN11 / COMFMN11", # Business Economics-II
    "BCH-223": "COMFMJ31 / COMMV31", # Specialised Accounts-II -> Specialised Accounting
    "BCH-224": "COMMN41 / COMFMN81", # Business Mathematics -> Business Statistics
    "BCH-225": "COMSE31 / COMFSE22", # Public Finance
    "BCH-226": "COMMN41 / COMFMN41", # Business Statistics
    
    # Semester 5
    "BCF-311": "COMFMJ64", # Security Analysis -> Security Analysis & Portfolio Management
    "BCF-312": "COMFMJ54 / COMMJE65", # Fund Based Financial Services -> Financial Services
    "BCF-313": "COMFMJ54 / COMMJE65", # Mutual Fund Operations -> Financial Services
    "BCF-314": "COMFMJ52 / COMMJE55", # New Issue Market Operations -> Financial Markets & Institutions
    "BCF-315": "COMFMJ74", # Stock Market Operations
    "BCH-311": "COMFMJ51 / COMMJ51", # Advanced Company Accounts
    "BCH-312": "COMMV51 / COMFMV51", # Income Tax Law & Accounts
    "BCH-313": "COMMJ62", # Company Law
    "BCH-314": "COMMJ82", # Banking Law and Practice
    "BCH-315": "COMSE32 / COMFMJ53", # Auditing
    "BCH-316": "COMMJ63 / COMFMJ83", # Business Ethics and Corporate Governance
    
    # Semester 6
    "BCF-321": "COMFMJ64", # Portfolio Management -> Security Analysis & Portfolio Management
    "BCF-322": "COMFMJ82 / COMMJE75", # Foreign Exchange Market Operations -> International Financial Management / Risk Management
    "BCF-323": "COMFMJ81 / COMMJE75", # Derivatives Market Operations -> Derivatives & Risk Management
    "BCF-324": "COMFMJ82", # International Financial Market Operations
    "BCF-325": "COMFMJ52 / COMMJE55", # Money Market Operations -> Financial Markets & Institutions
    "BCH-321": "COMFMJ61 / COMMJ61", # Financial Analysis
    "BCH-322": "COMFMV61 / COMMV61", # Indirect Tax -> GST and Customs Duty
    "BCH-323": "COMMJ62", # Secretarial Practice -> Company Law & Secretarial Practices
    "BCH-324": "COMMJ82", # Principles of Insurance -> Banking Laws and Insurance
    "BCH-B326": "COMMJ82", # Indian Banking System
    "BCH-B327": "COMMJ82", # Law & Practice of Insurance
    "BCH-F326": "COMFMJ52 / COMMJE55", # Financial Markets in India
    "BCH-F327": "COMMJE65", # Financial Services
    "BCH-I326": "COMMJ82 / COMMJ44 / COMMJE77", # Industrial Relations and Labour Laws -> Industrial Relations / Indian Labour Codes
    "BCH-I327": "COMMJE57", # Labour Welfare and Social Security
    "BCH-M326": "COMMJE56", # Sales Management and Advertising -> Advertising and Sales Management
    "BCH-M327": "COMMNE73", # International Marketing
    "ECH-M327": "COMMNE73", # International Marketing
}

def run():
    # 1. Load parsed commerce files
    with open('scratch/commerce_parsed.json', 'r') as f:
        parsed_papers = json.load(f)
        
    print(f"Loaded {len(parsed_papers)} parsed commerce papers.")
    
    # 2. Build list of new nep-data.js objects
    new_entries = []
    unmapped_count = 0
    
    for paper in parsed_papers:
        old_code = paper['code']
        
        # Look up NEP Code in mapping dictionary
        nep_code = MAPPING_DICTIONARY.get(old_code)
        if not nep_code:
            print(f"WARNING: Unmapped old code '{old_code}' for file {paper['fileName']}")
            unmapped_count += 1
            nep_code = "COMMJ11" # generic fallback
            
        entry = {
            "code": old_code,
            "subject": paper['subject'],
            "semester": paper['semester'],
            "year": paper['year'],
            "department": "Commerce",
            "filePath": paper['filePath'],
            "fileName": paper['fileName'],
            "nepCode": nep_code,
            "oldCode": old_code
        }
        new_entries.append(entry)
        
    print(f"Mapped {len(new_entries)} entries. Unmapped count: {unmapped_count}")
    
    # 3. Load existing js/nep-data.js content
    nep_data_path = 'js/nep-data.js'
    with open(nep_data_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract the array text
    array_match = re.search(r'export const NEP_LATEX_PYQ_DATA = (\[[\s\S]*?\]);', content)
    if not array_match:
        raise ValueError("Could not find NEP_LATEX_PYQ_DATA array in js/nep-data.js")
        
    array_json = array_match.group(1)
    existing_data = json.loads(array_json)
    print(f"Existing js/nep-data.js has {len(existing_data)} entries.")
    
    # 4. Remove any existing commerce entries from the array to prevent duplicates
    cleaned_data = [e for e in existing_data if e.get('department') != 'Commerce']
    print(f"Cleaned dataset: {len(cleaned_data)} entries.")
    
    # 5. Combine and sort by department, semester, and code
    combined_data = cleaned_data + new_entries
    combined_data.sort(key=lambda x: (x.get('department', ''), x.get('semester', 1), x.get('code', '')))
    
    # 6. Write back to js/nep-data.js
    new_array_json = json.dumps(combined_data, indent=2)
    new_content = f"export const NEP_LATEX_PYQ_DATA = {new_array_json};\n"
    
    with open(nep_data_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully updated js/nep-data.js with {len(combined_data)} total entries!")

if __name__ == '__main__':
    run()
