
from concurrent.futures import ProcessPoolExecutor
from collections import defaultdict
import os
import fitz
import nltk

#nltk.download('punkt')

def process_pdf(pdf_path):
    try:
        text = extract_text_from_pdf(pdf_path)
        update_index(index, text, pdf_path)
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

def build_index_parallel(root_folder):
    index = defaultdict(list)

    with ProcessPoolExecutor() as executor:
        pdf_paths = [os.path.join(root_folder, filename) for filename in os.listdir(root_folder) if filename.lower().endswith('.pdf')]
        executor.map(process_pdf, pdf_paths)

    return index

# Rest of your code remains unchanged
def build_index(root_folder):
    index = defaultdict(list)
    
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(foldername, filename)
                try:
                    text = extract_text_from_pdf(pdf_path)
                    update_index(index, text, pdf_path)
                except Exception as e:
                    print(f"Error processing {pdf_path}: {e}")
    return index

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ''.join(page.get_text() for page in doc)
    return text

def update_index(index, text, pdf_path):
    index[text.lower()].append(pdf_path)
    
def search_index(index, query):
    file_list = list()
    file_page = defaultdict(list)
    
    query_tokens = set(nltk.word_tokenize(query.lower()))

    for text, pdf_paths in index.items():
        text_tokens = set(nltk.word_tokenize(text.lower()))

        if query_tokens.issubset(text_tokens):
            file_list.extend(pdf_paths)
            
            for pdf_path in pdf_paths:
                with fitz.open(pdf_path) as doc:
                    for page_num, page in enumerate(doc, start=1):
                        page_text = page.get_text()
                        
                        if query_tokens.issubset(nltk.word_tokenize(page_text.lower())):
                            file_page[pdf_path].append(page_num)

    return file_page

# Example usage
root_folder = '/workspaces/FULL/media/media'
index = build_index(root_folder)

query = ''' what is server
'''
results = search_index(index, query)

if results:
    print(f"String found in the following PDF files:")
    for pdf_file, page_numbers in results.items():
        print(f"{pdf_file} - Page Numbers: {page_numbers}")
else:
    print("String not found in any PDF files.")