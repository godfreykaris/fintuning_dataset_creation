import os
import time
from multiprocessing import Pool, cpu_count
import pytesseract
from pdf2image import convert_from_path
import pdfplumber


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

def process_pdf(pdf_file, output_text_file, use_ocr=True, chunk_size=4):
    start_time = time.time()
    current_page = 1
    current_line = 1
    
    with Pool(cpu_count()) as pool:
        with open(output_text_file, 'a') as text_file:
            with open(pdf_file, 'rb') as f:
                while True:
                    pdf_images = convert_from_path(pdf_file, 300, first_page=current_page, last_page=(chunk_size if current_page == 1 else current_page + chunk_size - 1))
                    total_pages = len(pdf_images)

                    if total_pages == 0:
                        break

                    print("Total pages:", total_pages)

                    if use_ocr:
                        extracted_texts = pool.map(process_page_ocr, pdf_images)
                    else:
                        with pdfplumber.open(pdf_file) as pdf:
                           pages = pdf.pages[current_page - 1:current_page + total_pages - 1]
                           extracted_texts = [process_page_pdfplumber(page) for page in pages]
                            
                    for page_num, extracted_text in enumerate(extracted_texts, start=current_page):
                        lines = extracted_text.split('\n')
                        text_file.write(f"--- Beginning of Page {page_num} ---\n")
                        for line in lines:

                            ############################################################
                            current_time = time.time()  # Current time as a dummy timestamp, in a real deposition it would already be in the text
                            ############################################################

                            # Write line with line number and dummy timestamp
                            text_file.write(f"Line {current_line}, {time.strftime('%H:%M:%S', time.localtime(current_time))}: {line}\n")
                            current_time += 1  # Increment the dummy timestamp
                            current_line += 1  # Increment the line number
                        text_file.write(f"--- End of Page {page_num} ---\n\n")

                    current_page += total_pages
                    print(f"Processed {current_page - 1} pages in {time.time() - start_time} seconds")

def process_pdf_files(input_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.pdf'):
                pdf_file = os.path.join(root, file)
                output_text_file = pdf_file.replace('.pdf', '.txt')

                # Determine whether to use OCR based on the filename
                use_ocr_pdf = 'ocr' in file.lower()

                process_pdf(pdf_file, output_text_file, use_ocr_pdf)

if __name__ == '__main__':
    
    pdf_source_folder = "sample_source"     

    process_pdf_files(pdf_source_folder)
