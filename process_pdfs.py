import os
import time
from multiprocessing import Pool, cpu_count
import pytesseract
from pdf2image import convert_from_path
import pdfplumber
import re

# Function to process a single page and extract text using OCR
def process_page_ocr(page_image):
    # Use Tesseract OCR to extract text from the page image
    text = pytesseract.image_to_string(page_image)
    # Remove empty lines from the extracted text
    non_empty_lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(non_empty_lines)

# Function to process a single page and extract text using pdfplumber
def process_page_pdfplumber(page):
    text = page.extract_text()
    # Remove empty lines from the extracted text
    non_empty_lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(non_empty_lines)

# Example filename: deposition-ocr-1.pdf
def determine_num_sections(file_name):
    # Extract the last part of the filename after splitting by '-'
    last_part = file_name.split('-')[-1]

    # Try to find the section number
    section_numbers = re.findall(r'\d+', last_part)

    if section_numbers:
        # If section number is found, return the first one
        return int(section_numbers[0])
    else:
        # If no section number is found, default to 1
        return 1
    
# Function to split the image into specified sections
def split_pdf_image(pdf_page_image, num_sections):
    width, height = pdf_page_image.size
    if num_sections == 2:
        section1 = pdf_page_image.crop((0, 0, width//2, height))
        section2 = pdf_page_image.crop((width//2, 0, width, height))
        return [section1, section2]
    elif num_sections == 4:
        # Split the page vertically and horizontally into four sections
        section1 = pdf_page_image.crop((0, 0, width//2, height // 2))
        section2 = pdf_page_image.crop((0, height // 2, width//2, height))
        section3 = pdf_page_image.crop((width//2, 0, width, height // 2))
        section4 = pdf_page_image.crop((width//2, height // 2, width, height))
        return [section1, section2, section3, section4]
    
# Function to split the pdf into specified sections
def split_normal_pdf(pdf_page, num_sections):
    width, height = pdf_page.width, pdf_page.height
    if num_sections == 2:
        # Split the page vertically into two sections
        section1 = pdf_page.within_bbox((0, 0, width//2, height // 2))
        section2 = pdf_page.within_bbox((0, height // 2, width, height))
        return [section1, section2]
    
    elif num_sections == 4:
        # Split the page vertically and horizontally into four sections
        section1 = pdf_page.within_bbox((0, 0, width // 2, height // 2))
        section2 = pdf_page.within_bbox((0, height // 2, width // 2, height))
        section3 = pdf_page.within_bbox((width // 2, 0, width, height // 2))
        section4 = pdf_page.within_bbox((width // 2, height // 2, width, height))
        return [section1, section2, section3, section4]

def write_extracted_text(text_file, extracted_texts, current_page):
    for page_num, extracted_text in enumerate(extracted_texts, start=current_page):
        lines = extracted_text.split('\n')
        text_file.write(f"--- Beginning of Page {page_num} ---\n")

        current_line = 1
        for line in lines:
            # Check if the line contains only numbers
            if not re.match(r'^\d+$', line.strip()):
                # Check if the line starts with a number followed by whitespace
                if re.match(r'^\d+\s', line):
                    # Strip off the number and whitespace as they are line numbers
                    line = re.sub(r'^\d+\s', '', line)

                current_time = time.time()  # Current time as a dummy timestamp
                text_file.write(f"Line {current_line}, {time.strftime('%H:%M:%S', time.localtime(current_time))}: {line}\n")
                current_line += 1  # Increment the line number

        text_file.write(f"--- End of Page {page_num} ---\n\n")

def process_pdf(pdf_file, output_text_file,num_sections=1, use_ocr=True, chunk_size=4):
    start_time = time.time()
    current_page = 1
    
    utilised_cores = min(chunk_size, cpu_count())

    with Pool(utilised_cores) as pool:
        with open(output_text_file, 'a') as text_file:
            with open(pdf_file, 'rb') as f:
                while True:
                                        
                    if use_ocr:
                        pdf_page_images = convert_from_path(pdf_file, 300, first_page=current_page, last_page=(chunk_size if current_page == 1 else current_page + chunk_size - 1))
                        total_pages = len(pdf_page_images)

                        if total_pages == 0:
                            break
                        
                        if(num_sections > 1):
                            # Split each PDF page image into the specified individual sections
                            split_pdf_pages_images = []
                            for pdf_page_image in pdf_page_images:
                                split_pages = split_pdf_image(pdf_page_image, num_sections)
                                # Extend the list with all four sections
                                split_pdf_pages_images.extend(split_pages)

                            extracted_texts = pool.map(process_page_ocr, split_pdf_pages_images)
                        else:
                            extracted_texts = pool.map(process_page_ocr, pdf_page_images)
                    else:
                        with pdfplumber.open(pdf_file) as pdf:
                           pages = pdf.pages[current_page - 1:current_page + chunk_size - 1]
                           
                           total_pages = len(pages)
                           if(total_pages == 0):
                               break
                           
                           if(num_sections > 1):
                               # Split each PDF page into the specified individual sections
                               split_pdf_pages = []
                               for pdf_page in pages:
                                   split_pages = split_normal_pdf(pdf_page, num_sections)
                                    # Extend the list with all four sections
                                   split_pdf_pages.extend(split_pages)
   
                                   extracted_texts = [process_page_pdfplumber(page) for page in split_pdf_pages]
                                      
                           else:
                              extracted_texts = [process_page_pdfplumber(page) for page in pages]
                    
                    write_extracted_text(text_file, extracted_texts, current_page)
                                            
                    current_page += chunk_size
                    print(f"Processed {current_page - 1} pages in {time.time() - start_time} seconds")

def process_pdf_files(input_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.pdf'):
                pdf_file = os.path.join(root, file)
                output_text_file = pdf_file.replace('.pdf', '.txt')

                # Determine the number of sections based on the filename
                num_sections = determine_num_sections(file)

                # Determine whether to use OCR based on the filename
                use_ocr_pdf = 'ocr' in file.lower()

                process_pdf(pdf_file, output_text_file, num_sections, use_ocr_pdf)

if __name__ == '__main__':
    
    pdf_source_folder = "test_depositions"     

    process_pdf_files(pdf_source_folder)
