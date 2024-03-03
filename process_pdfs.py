# import pytesseract
# from pdf2image import convert_from_path
# from multiprocessing import Pool, cpu_count

# # Path to the PDF file
# pdf_file = 'sample_source/sample_deposition_of_plaintiff.pdf'
# output_text_file = 'sample_source/extracted_text.txt'  # Path to the output text file
# chunk_size = 10  # Process 10 pages at a time

# # Function to process a single page and extract text
# def process_page(page_image):
#     # Use Tesseract OCR to extract text from the page image
#     text = pytesseract.image_to_string(page_image)
    
#     # Remove empty lines from the extracted text
#     lines = text.strip().split('\n')
#     non_empty_lines = [line for line in lines if line.strip()]
    
#     # Return non-empty lines
#     return '\n'.join(non_empty_lines)

# if __name__ == '__main__':
#     # Initialize the Pool with the number of available CPU cores
#     with Pool(cpu_count()) as pool:
#         # Open the output text file in append mode
#         with open(output_text_file, 'a') as text_file:
#             # Iterate through PDF in chunks
#             with open(pdf_file, 'rb') as f:
#                 while True:
#                     # Read the next chunk of pages
#                     pdf_images = convert_from_path(pdf_file, 300, first_page=None, last_page=chunk_size)
                    
#                     print("Total pages:", len(pdf_images))
#                     # If no pages are left, break the loop
#                     if len(pdf_images) == 0:
#                         break
                    
#                     # Process each page in the chunk using multiprocessing
#                     extracted_texts = pool.map(process_page, pdf_images)
                    
#                     # Write the extracted texts to the output text file
#                     for extracted_text in extracted_texts:
#                         text_file.write(extracted_text)
#                         text_file.write('\n')  # Add a newline after each page's text
                    
#                     # Print progress
#                     print(f"Processed {len(pdf_images)} pages")


import pdfplumber
import time

# Path to the PDF file
pdf_file = 'sample_source/test.pdf'

start_time = time.time()

# Open the PDF file
with pdfplumber.open(pdf_file) as pdf:
    # Initialize an empty string to store the extracted text
    extracted_text = ''
    
    # Iterate through each page of the PDF
    for page in pdf.pages:
        # Extract text from the page
        page_text = page.extract_text()
        
        # Append the extracted text to the overall text
        extracted_text += page_text

# Print or process the extracted text
print(extracted_text)

print("\nTime taken:", time.time() - start_time)
