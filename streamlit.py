import streamlit as st
from main import TextExtractor

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