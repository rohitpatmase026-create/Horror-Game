import os
import tempfile
from flask import Flask, request, send_file
from flask_cors import CORS
from pdf2docx import Converter
import pdfplumber
import pandas as pd
import io

app = Flask(__name__)
CORS(app) # Taaki aapki website bina block hue isse baat kar sake

@app.route('/convert/word', methods=['POST'])
def to_word():
    uploaded_file = request.files['file']
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, "input.pdf")
        docx_path = os.path.join(temp_dir, "output.docx")
        uploaded_file.save(pdf_path)
        
        # 100% Accurate Python Converter
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()
        
        return send_file(docx_path, as_attachment=True)

@app.route('/convert/excel', methods=['POST'])
def to_excel():
    uploaded_file = request.files['file']
    excel_buffer = io.BytesIO()
    with pdfplumber.open(uploaded_file) as pdf:
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            for page_num, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                for t_idx, table in enumerate(tables):
                    df = pd.DataFrame(table)
                    if not df.empty and len(df) > 1:
                        df.columns = df.iloc[0]
                        df = df[1:]
                    df.to_excel(writer, sheet_name=f"Page{page_num}_Table{t_idx+1}"[:31], index=False)
    excel_buffer.seek(0)
    return send_file(excel_buffer, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
