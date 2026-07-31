import fitz
import os
import shutil

def add_clickable_footer_links():
    pdf_path = 'BHU_BSc_Mathematics_Complete_Syllabus.pdf'
    out_path = 'BHU_BSc_Mathematics_Complete_Syllabus_temp.pdf'
    
    doc = fitz.open(pdf_path)
    print(f"Adding sciqb.com footer link to all {len(doc)} pages...")

    for page in doc:
        rect = page.rect
        width = rect.width
        height = rect.height

        # Draw text www.sciqb.com at bottom left
        text_point = fitz.Point(40, height - 20)
        
        page.insert_text(
            text_point,
            "www.sciqb.com",
            fontname="helv",
            fontsize=9,
            color=(0.01, 0.52, 0.78) # #0284c7 blue
        )

        # Create clickable link rectangle around "www.sciqb.com"
        link_rect = fitz.Rect(35, height - 32, 135, height - 12)
        page.insert_link({
            "kind": fitz.LINK_URI,
            "from": link_rect,
            "uri": "https://www.sciqb.com"
        })

    doc.save(out_path)
    doc.close()
    
    shutil.move(out_path, pdf_path)
    print("Successfully added clickable www.sciqb.com link to every page!")

if __name__ == '__main__':
    add_clickable_footer_links()
