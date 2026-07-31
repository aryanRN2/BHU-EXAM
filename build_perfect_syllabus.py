import json
import os
import re
import subprocess

def roman(n):
    r_map = [(10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    res = ""
    for val, char in r_map:
        while n >= val:
            res += char
            n -= val
    return res if res else str(n)

def clean_id(text):
    return re.sub(r'[^a-zA-Z0-9]', '_', str(text))

def build_pdf():
    # 1. Load JSON
    json_path = 'SYLLABUS/maths_syllabus.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    dept = data.get('department', 'Department of Mathematics')
    univ = data.get('university', 'Banaras Hindu University')
    prog = data.get('programme', 'B.Sc. (Hons.) Mathematics')
    semesters = data.get('semesters', [])

    # 2. Load Raw Text to match References & Teaching Hours
    with open('extracted_raw_math_text.txt', 'r', encoding='utf-8', errors='ignore') as f:
        raw_text = f.read()

    splits = re.split(r'Course\s+Title\s+', raw_text)
    course_meta = {}
    for section in splits[1:]:
        lines = [l.strip() for l in section.split('\n') if l.strip()]
        if not lines:
            continue
        title_line = lines[0]
        code_match = re.match(r'([A-Z0-9_/]+)\s*:\s*(.*)', title_line)
        if code_match:
            c_code = code_match.group(1).strip()
            c_name = code_match.group(2).strip()
        else:
            c_code = "UNKNOWN"
            c_name = title_line

        # References
        ref_match = re.search(r'Texts\s*/\s*References\s*\n(.*?)Learning\s+Outcomes', section, re.DOTALL | re.IGNORECASE)
        references = []
        if ref_match:
            ref_raw = ref_match.group(1).strip()
            ref_items = re.split(r'\n(?=\d+\.\s+)', ref_raw)
            for ref in ref_items:
                clean_ref = ref.strip().replace('\n', ' ')
                if clean_ref:
                    references.append(clean_ref)

        norm_key = re.sub(r'[^A-Z0-9]', '', c_code.upper())
        if norm_key not in course_meta:
            course_meta[norm_key] = {
                "references": references
            }

    # Calculate page mapping for TOC
    current_page = 3
    toc_mapping = []

    for sem in semesters:
        s_num = sem.get('semester')
        papers = sem.get('papers', [])
        sem_papers_mapping = []

        for p_idx, p in enumerate(papers):
            p_code = p.get('code', 'N/A')
            p_name = p.get('name', 'Course')
            anchor = f"course_{s_num}_{clean_id(p_code)}_{p_idx}"
            sem_papers_mapping.append({
                "code": p_code,
                "name": p_name,
                "anchor": anchor,
                "page": current_page,
                "subnum": f"{s_num}.{p_idx+1}"
            })
            current_page += 1

        toc_mapping.append({
            "sem": s_num,
            "papers": sem_papers_mapping
        })

    # HTML Construction without CSS bottom-left text to prevent any double text overlap
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{prog} - Syllabus | {univ}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap');

        @page {{
            size: A4;
            margin: 16mm 16mm 18mm 16mm;
            @bottom-right {{
                content: counter(page);
            }}
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: 'Crimson Pro', 'Times New Roman', Times, serif;
            color: #000000;
            line-height: 1.45;
            font-size: 11pt;
            background: #ffffff;
            margin: 0;
            padding: 0;
        }}

        /* Running Header */
        .running-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #000000;
            padding-bottom: 4px;
            margin-bottom: 18px;
            font-size: 9.5pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
        }}

        /* Title Block */
        .title-block {{
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #000000;
        }}

        .univ-name {{
            font-size: 16pt;
            font-weight: 700;
        }}

        .dept-name {{
            font-size: 13pt;
            font-weight: 600;
            margin-top: 2px;
        }}

        .prog-name {{
            font-size: 18pt;
            font-weight: 700;
            margin-top: 6px;
        }}

        .sub-name {{
            font-size: 11.5pt;
            font-style: italic;
            margin-top: 4px;
        }}

        /* Classic Blue Hyperlinked TOC */
        .toc-container {{
            margin-bottom: 20px;
        }}

        .toc-main-title {{
            font-size: 16pt;
            font-weight: 700;
            color: #0284c7;
            border-bottom: 1.5px solid #0284c7;
            padding-bottom: 4px;
            margin-bottom: 14px;
            font-family: 'Inter', sans-serif;
        }}

        .toc-sem-header {{
            font-size: 12pt;
            font-weight: 700;
            color: #000000;
            margin-top: 10px;
            margin-bottom: 6px;
        }}

        .toc-entry {{
            display: flex;
            align-items: baseline;
            margin-bottom: 4px;
            font-size: 10.5pt;
        }}

        .toc-link {{
            color: #0284c7;
            text-decoration: none;
            display: flex;
            align-items: baseline;
            width: 100%;
        }}

        .toc-link:hover {{
            text-decoration: underline;
        }}

        .toc-subnum {{
            font-weight: 600;
            min-width: 28px;
            color: #000000;
        }}

        .toc-text {{
            color: #0284c7;
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .toc-dots {{
            flex-grow: 1;
            border-bottom: 1px dotted #94a3b8;
            margin: 0 8px 3px 8px;
        }}

        .toc-page {{
            font-weight: 700;
            color: #000000;
            white-space: nowrap;
        }}

        .page-break {{
            page-break-after: always;
        }}

        /* Paper Syllabus Table */
        .paper-page {{
            page-break-before: always;
            padding-top: 6px;
        }}

        .official-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 14px;
            font-size: 11pt;
            background: #ffffff;
        }}

        .official-table td, .official-table th {{
            border: 1px solid #000000;
            padding: 7px 10px;
            vertical-align: top;
        }}

        .official-table th {{
            background: #ffffff;
            font-weight: 700;
            font-size: 11.5pt;
            text-align: center;
        }}

        .col-units {{
            width: 12%;
            text-align: center;
            font-weight: 700;
            font-size: 11.5pt;
        }}

        .col-content {{
            width: 73%;
            text-align: left;
            line-height: 1.45;
        }}

        .col-hours {{
            width: 15%;
            text-align: center;
            font-weight: 700;
            font-size: 11.5pt;
        }}

        .header-cell-title {{
            font-weight: 700;
            width: 25%;
            background: #ffffff;
        }}

        .header-cell-val {{
            font-weight: 600;
            width: 75%;
        }}

        .ref-list {{
            margin: 0;
            padding-left: 18px;
        }}

        .ref-list li {{
            margin-bottom: 3px;
            line-height: 1.4;
        }}
    </style>
</head>
<body>

    <!-- Running Header -->
    <div class="running-header">
        <span>Banaras Hindu University — Department of Mathematics</span>
        <span>B.Sc. (Hons.) Mathematics</span>
    </div>

    <!-- Title Block -->
    <div class="title-block">
        <div class="univ-name">{univ}</div>
        <div class="dept-name">{dept}</div>
        <div class="prog-name">{prog}</div>
        <div class="sub-name">Detailed Syllabus under NEP 2020 (Semesters I – VIII)</div>
    </div>

    <!-- Classic Blue Hyperlinked Table of Contents -->
    <div class="toc-container">
        <div class="toc-main-title">Contents</div>
"""

    for sem_info in toc_mapping:
        s_num = sem_info['sem']
        papers_map = sem_info['papers']

        html_content += f"""
        <div class="toc-sem-header">{s_num} &nbsp; Semester {s_num}</div>
"""
        for p_info in papers_map:
            p_code = p_info['code']
            p_name = p_info['name']
            anchor = p_info['anchor']
            pg_num = p_info['page']
            subnum = p_info['subnum']

            html_content += f"""
        <div class="toc-entry">
            <a href="#{anchor}" class="toc-link" title="Jump to {p_code} syllabus">
                <span class="toc-subnum">{subnum}</span>
                <span class="toc-text">{p_code}: {p_name}</span>
                <span class="toc-dots"></span>
                <span class="toc-page">{pg_num}</span>
            </a>
        </div>
"""

    html_content += """
    </div>

    <!-- Individual Course Syllabus Pages -->
"""

    for sem in semesters:
        s_num = sem.get('semester')
        papers = sem.get('papers', [])

        for p_idx, p in enumerate(papers):
            p_code = p.get('code', 'N/A')
            p_name = p.get('name', 'Course')
            p_credits = p.get('credits', '-')
            p_type = p.get('course_type', 'Core')
            syllabus_units = p.get('syllabus', [])

            norm_code = re.sub(r'[^A-Z0-9]', '', str(p_code).upper())
            meta = course_meta.get(norm_code, {})
            refs = meta.get("references", [])
            anchor = f"course_{s_num}_{clean_id(p_code)}_{p_idx}"

            html_content += f"""
    <div class="paper-page" id="{anchor}">
        <!-- Top Course Header Table -->
        <table class="official-table">
            <tr>
                <td class="header-cell-title">Course Title</td>
                <td class="header-cell-val" style="font-size: 11.5pt; font-weight: 700;">{p_code}: {p_name}</td>
            </tr>
            <tr>
                <td class="header-cell-title">Credits & Type</td>
                <td class="header-cell-val">Course Type: <strong>{p_type}</strong> &nbsp;|&nbsp; Total Credits: <strong>{p_credits}</strong></td>
            </tr>
        </table>

        <!-- Main Units Grid Table -->
        <table class="official-table">
            <thead>
                <tr>
                    <th class="col-units">Units</th>
                    <th class="col-content" style="text-align: left;">CourseContent</th>
                    <th class="col-hours">Hr.of Teaching</th>
                </tr>
            </thead>
            <tbody>
"""
            for u_idx, unit in enumerate(syllabus_units):
                u_num = unit.get('unit', u_idx + 1)
                try:
                    u_roman = roman(int(u_num))
                except:
                    u_roman = str(u_num)

                u_topics = unit.get('topics', '')
                hr_match = re.search(r'\s+(\d+)\s*$', u_topics)
                if hr_match:
                    hrs = hr_match.group(1)
                    clean_topics = u_topics[:hr_match.start()].strip()
                else:
                    hrs = "12" if int(p_credits) >= 4 else "15"
                    clean_topics = u_topics.strip()

                html_content += f"""
                <tr>
                    <td class="col-units">{u_roman}</td>
                    <td class="col-content">{clean_topics}</td>
                    <td class="col-hours">{hrs}</td>
                </tr>
"""
            html_content += """
            </tbody>
        </table>
"""

            if refs:
                html_content += """
        <!-- References Table -->
        <table class="official-table">
            <tr>
                <td style="width: 25%; font-weight: 700; background: #ffffff;">Texts / References</td>
                <td style="width: 75%;">
                    <ol class="ref-list">
"""
                for ref in refs:
                    html_content += f"                        <li>{ref}</li>\n"
                html_content += """
                    </ol>
                </td>
            </tr>
        </table>
"""

            html_content += """
    </div>
"""

    html_content += """
</body>
</html>
"""

    html_file = 'maths_perfect_syllabus.html'
    pdf_file = 'BHU_BSc_Mathematics_Complete_Syllabus.pdf'

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML generated at {html_file}")

    # Convert to PDF using Google Chrome CLI
    chrome_cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_file}",
        "--no-pdf-header-footer",
        os.path.abspath(html_file)
    ]
    
    res = subprocess.run(chrome_cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(pdf_file):
        print(f"PDF successfully created: {pdf_file} (Size: {os.path.getsize(pdf_file)} bytes)")

if __name__ == '__main__':
    build_pdf()
