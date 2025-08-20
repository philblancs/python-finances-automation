import streamlit as st
import pandas as pd
import pdfplumber
import pytesseract
from PIL import Image
import os

st.set_page_config(page_title="Transaction Uploader", page_icon="📂", layout="centered")

def pdf_to_csv(pdf_file, output_csv="converted.csv"):
    """Convert a PDF bank statement to CSV using pdfplumber, fallback to OCR if needed."""
    all_data = []
    ocr_texts = []

    try:
        with pdfplumber.open(pdf_file) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                try:
                    table = page.extract_table()
                    if table:
                        all_data.extend(table)
                    else:
                        print(f"[DEBUG] No table found on page {i}, trying OCR...")
                        # Convert page to image and OCR it
                        page_img = page.to_image(resolution=300).original
                        text = pytesseract.image_to_string(page_img)
                        if text.strip():
                            ocr_texts.append(text)
                except Exception as e:
                    print(f"[ERROR] Failed to process page {i}: {e}")
    except Exception as e:
        print("[CRITICAL] Could not open PDF:", e)
        return None

    if all_data:
        try:
            df = pd.DataFrame(all_data[1:], columns=all_data[0])
            df.to_csv(output_csv, index=False)
            return output_csv
        except Exception as e:
            print("[ERROR] Failed to create DataFrame:", e)
            return None
    elif ocr_texts:
        # Save OCR text as CSV (line by line)
        try:
            with open(output_csv, "w", encoding="utf-8") as f:
                for text in ocr_texts:
                    for line in text.splitlines():
                        if line.strip():
                            f.write(line.replace("\t", ",") + "\n")
            return output_csv
        except Exception as e:
            print("[ERROR] Failed to save OCR text:", e)
            return None
    else:
        print("[WARNING] No data extracted from PDF (tables or OCR)")
        return None

def main():
    st.title("Transaction File Uploader")

    file_type = st.radio(
        "Select the type of file you want to upload:",
        ("CSV", "PDF")
    )

    uploaded_file = st.file_uploader("Upload your file", type=["csv", "pdf"])

    if uploaded_file:
        if file_type == "CSV":
            if uploaded_file.name.endswith(".csv"):
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success("CSV file uploaded successfully ✅")
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"Failed to read CSV: {e}")
            else:
                st.error("The uploaded file is not a CSV. Please upload a valid CSV file.")
        
        elif file_type == "PDF":
            if uploaded_file.name.endswith(".pdf"):
                temp_pdf = "temp_uploaded.pdf"
                with open(temp_pdf, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                csv_path = pdf_to_csv(temp_pdf, "converted.csv")
                if csv_path and os.path.exists(csv_path):
                    try:
                        df = pd.read_csv(csv_path)
                        st.success("PDF converted to CSV successfully ✅")
                        st.dataframe(df.head())
                    except Exception as e:
                        st.warning("OCR extracted text but couldn’t structure it as a table.")
                        with open(csv_path, "r", encoding="utf-8") as f:
                            st.text_area("Extracted OCR Text:", f.read(), height=300)
                else:
                    st.error("Could not extract data from this PDF. It may be corrupted.")
            else:
                st.error("The uploaded file is not a PDF. Please upload a valid PDF file.")

if __name__ == "__main__":
    main()
