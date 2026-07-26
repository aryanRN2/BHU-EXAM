import json

with open('/Users/aryanmaurya/exam portal/scratch/commerce_parsed.json', 'r') as f:
    papers = json.load(f)

# Group by unique code
unique_papers = {}
for p in papers:
    code = p['code']
    subject = p['subject']
    sem = p['semester']
    if code not in unique_papers:
        unique_papers[code] = {
            'subject': subject,
            'semester': sem,
            'years': []
        }
    unique_papers[code]['years'].append(p['year'])

print("Unique Commerce Papers in COMMERCE_LATEX:")
for code in sorted(unique_papers.keys()):
    info = unique_papers[code]
    years_str = ", ".join(sorted(list(set(info['years']))))
    print(f"Code: {code} | Semester: {info['semester']} | Subject: {info['subject']} | Years: {years_str}")
