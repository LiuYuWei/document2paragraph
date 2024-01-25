import os
import streamlit as st
import fitz  # PyMuPDF
import re
import csv
import time
import os
import docx  # python-docx
from io import StringIO

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
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"資料夾 '{folder_name}' 已創建。")
        csv_file_name = f"{folder_name}/{file_base_name}_{int(time.time())}.csv"

        # 寫入CSV檔案
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['text', 'file_name'])
            writer.writeheader()
            for item in data:
                writer.writerow({'text': item, 'file_name': self.file_path})

        return csv_file_name
    
    def get_csv_data(self, data):
        # 使用 StringIO 來建立 CSV 格式的字符串
        csv_stringio = StringIO()
        writer = csv.DictWriter(csv_stringio, fieldnames=['text', 'file_name'])
        writer.writeheader()
        for item in data:
            writer.writerow({'text': item, 'file_name': self.file_path})
        
        # 將 StringIO 內容轉換為字節串
        csv_string = csv_stringio.getvalue()
        csv_bytes = csv_string.encode()
        return csv_bytes

# Streamlit界面
st.title('文檔內容提取器')

# 文件上傳
uploaded_file = st.file_uploader("選擇一個PDF或DOCX文件", type=["pdf", "docx"])

# 分割模式輸入
pattern = st.text_input("輸入分割標題的模式", '(\s*[一二三四五六七八九十]{1,3}\、)')

# 提交按鈕
if st.button('提交'):
    if uploaded_file is not None:
        # 儲存文件到本地
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 初始化提取器
        extractor = TextExtractor(uploaded_file.name)
        text = extractor.extract_text()
        split_sections = extractor.split_text_by_titles(pattern=pattern)
        
        # 顯示提取的文本和分割的部分
        # st.write("提取的文本:")
        # st.text_area("Extracted Text", text, height=300)
        st.write("分割的部分:")
        st.write(split_sections)

        # 將分割的部分轉換為CSV的字節串並創建下載按鈕
        csv_bytes = extractor.get_csv_data(split_sections)
        st.download_button(
            label="下載CSV文件",
            data=csv_bytes,
            file_name='extracted_text.csv',
            mime='text/csv'
        )
    else:
        st.error("請上傳一個文件。")