# document2paragraph

You can use the python script to transfer pdf, docx, and other documents to paragraph for transferring them to embedding vector. This tool is particularly useful for scenarios where text extraction and further processing from various documents are required.

## Features

- Supports text extraction from PDF and DOCX files.
- Allows custom title patterns for segmenting text.
- Saves extracted text into a CSV file for further processing.

## Installation

Before using the `document2paragraph` tool, ensure that you have Python 3 installed. Follow these steps to install the necessary dependencies:

```bash
git clone https://github.com/LiuYuWei/document2paragraph.git
cd document2paragraph
pip install -r requirements.txt
```

## Usage

To use the `document2paragraph` tool, follow these steps:

1. Place your PDF or DOCX files in an appropriate directory.
2. Execute the script with the following command:

```bash
python main.py <document_file_path> --pattern <split_pattern> --folder <output_folder>
```

For example:

```bash
python main.py example.pdf --pattern "(\s*[一二三四五六七八九十]{1,3}\、)" --folder result
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
