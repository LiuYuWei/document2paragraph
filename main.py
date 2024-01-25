import fitz  # PyMuPDF
import re
import csv
import time
import os
import argparse
import docx  # python-docx

class TextExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""

    def extract_text(self):
        file_extension = os.path.splitext(self.file_path)[1].lower()
        if file_extension == '.pdf':
            print("This is PDF file.")
            self.text = self.extract_text_from_pdf()
        elif file_extension == '.docx':
            print("This is docx file.")
            self.text = self.extract_text_from_docx()
        else:
            raise ValueError("Unsupported file type. Please provide a PDF or DOCX file.")
        return self.text

    def extract_text_from_pdf(self):
        # 打開PDF文件
        doc = fitz.open(self.file_path)

        # 遍歷每一頁
        for page in doc:
            self.text += page.get_text()
        doc.close()
        
        return self.text

    def extract_text_from_docx(self):
        doc = docx.Document(self.file_path)
        
        self.text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return self.text

    def split_text_by_titles(self, pattern):
        # 使用正則表達式匹配模式並分割文本
        pattern = r"{}".format(pattern)
        parts = re.split(pattern, self.text)[1:]  # 分割文本並去除第一個空字符串
        
        # 將標題和相應的文本合併
        result = [parts[i] + parts[i + 1] for i in range(0, len(parts) - 1, 2)]
        
        return result

    def save_to_csv(self, data, folder_name="csv_file"):
        # 取得不含副檔名的PDF檔案名
        file_base_name = os.path.splitext(os.path.basename(self.file_path))[0]

        # 建立CSV檔案名稱
        csv_file_name = f"{folder_name}/{file_base_name}_{int(time.time())}.csv"

        # 寫入CSV檔案
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['text', 'file_name'])
            writer.writeheader()
            for item in data:
                writer.writerow({'text': item, 'file_name': self.file_path})

        return csv_file_name

def main(args):
    extractor = TextExtractor(args.file_path)
    text = extractor.extract_text()
    split_sections = extractor.split_text_by_titles(pattern=args.pattern)
    csv_file = extractor.save_to_csv(split_sections, folder_name=args.folder)
    print(f"CSV file saved as: {csv_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from a PDF or DOCX file and save it into a CSV file.")
    parser.add_argument("file_path", help="Path to the file (PDF or DOCX)")
    parser.add_argument("--pattern", default='(\s*[一二三四五六七八九十]{1,3}\、)', help="Pattern to split text by titles")
    parser.add_argument("--folder", default="csv_file", help="Folder name to save the CSV file")
    args = parser.parse_args()
    
    main(args)
