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


if __name__ == '__main__':
    # Path to the PDF file
    # pdf_file = 'sample_source/ocr-independent/test.pdf'
    # output_text_file = 'sample_source/ocr-independent/extracted_test.txt'  # Path to the output text file
    
    # pdf_file = 'sample_source/ocr-dependent/truck-accident-deposition.pdf'
    # output_text_file = 'sample_source/ocr-dependent/extracted_truck-accident-deposition.txt'
    
    pdf_file = 'sample_source/ocr-dependent/sample_deposition_of_plaintiff.pdf'
    output_text_file = 'sample_source/ocr-dependent/extracted_sample_deposition_of_plaintiff.txt'

    use_ocr = True  # Set this flag to True to use OCR, False to use pdfplumber
    
    chunk_size = 4
    current_page = 1
    start_time = time.time()

    # Initialize the Pool with the number of available CPU cores
    with Pool(cpu_count()) as pool:
        # Open the output text file in append mode
        with open(output_text_file, 'a') as text_file:
            # Iterate through PDF in chunks
            with open(pdf_file, 'rb') as f:
                while True:
                    # Read the next chunk of pages
                    pdf_images = convert_from_path(pdf_file, 300, first_page=current_page, last_page=(chunk_size if current_page == 1 else current_page + chunk_size - 1))
                    total_pages = len(pdf_images)

                    # If no pages are left, break the loop
                    if total_pages == 0:
                        break

                    print("Total pages:", total_pages)

                    if use_ocr:
                        # Process each page in the chunk using OCR and multiprocessing
                        extracted_texts = pool.map(process_page_ocr, pdf_images)
                    else:
                        # Use pdfplumber to extract text from each page
                        with pdfplumber.open(pdf_file) as pdf:
                           pages = pdf.pages[current_page - 1:current_page + total_pages - 1]
                           extracted_texts = [process_page_pdfplumber(page) for page in pages]


                    # Write the extracted texts to the output text file
                    for extracted_text in extracted_texts:
                        text_file.write(extracted_text)
                        text_file.write('\n')  # Add a newline after each page's text

                    current_page += total_pages
                    # Print progress
                    print(f"Processed {current_page - 1} pages in {time.time() - start_time} seconds")
