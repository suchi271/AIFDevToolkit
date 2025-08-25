from docx import Document

def check_actual_54_content():
    doc = Document('output/application_assessment_report.docx')
    
    print("=== Checking ACTUAL 5.4 Content ===\n")
    
    # Find the actual 5.4 heading (not TOC entry)
    found_real_54 = False
    content_lines = []
    
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        style = p.style.name
        
        # Look for the actual heading (should be Heading 1 style)
        if ('5.4' in text and 'Low Level Design' in text and 
            style.startswith('Heading')):
            found_real_54 = True
            print(f"Found REAL 5.4 heading at paragraph {i}: '{text}' (style: {style})")
            continue
        
        if found_real_54:
            # Stop at next section
            if text.startswith('6') and 'Architecture Heatmap' in text:
                print(f"Next section found at paragraph {i}: '{text}'")
                break
            
            # Collect content
            if text:
                content_lines.append(text)
    
    if found_real_54:
        print(f"\nActual content under 5.4 section:")
        print(f"Found {len(content_lines)} lines of content")
        
        if content_lines:
            for i, line in enumerate(content_lines[:10]):  # Show first 10 lines
                print(f"  {i+1}: {line[:100]}{'...' if len(line) > 100 else ''}")
            if len(content_lines) > 10:
                print(f"  ... and {len(content_lines) - 10} more lines")
        else:
            print("  NO CONTENT found under the actual 5.4 heading!")
    else:
        print("Could not find the actual 5.4 heading!")

if __name__ == "__main__":
    check_actual_54_content()
