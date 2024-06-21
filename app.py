import streamlit as st
from PIL import Image
import img2pdf
from pdf2jpg import pdf2jpg
import os
import io

def convert_jpeg_to_png(source_file, target_file):
    image = Image.open(source_file)
    image.save(target_file, format='PNG')

def convert_png_to_jpeg(source_file, target_file):
    image = Image.open(source_file)
    image = image.convert('RGB')
    image.save(target_file, format='JPEG')
    
def convert_jpeg_to_pdf(source_file, target_file):
    image = Image.open(source_file)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    pdf_bytes = img2pdf.convert(image_bytes.getvalue())
    with open(target_file, "wb") as file:
        file.write(pdf_bytes)

def convert_pdf_to_jpeg(source_file, output_dir):
    result = pdf2jpg.convert_pdf2jpg(source_file, output_dir, dpi=300, pages="ALL")
    return result[0]['output_jpgfiles']

# Streamlit UI
def main():
    """Streamlit application for image conversion"""

    # Title and description
    st.title("Image Converter")
    st.write("Convert between JPEG, PNG, and PDF formats.")

    # File upload selection
    file_type = st.selectbox("Select file type:", ("JPEG", "PNG", "PDF"))
    uploaded_file = st.file_uploader(f"Upload {file_type} file:", type=file_type.lower())

    # Conversion selection based on uploaded file type
    if uploaded_file is not None:
        if file_type == "JPEG":
            # Conversion options for JPEG
            convert_to = st.selectbox("Convert to:", ("PNG", "PDF"))
            if convert_to == "PNG":
                converted_file = f"{uploaded_file.name[:-4]}.png"
                if st.button("Convert to PNG"):
                    image = Image.open(uploaded_file)
                    buffer = io.BytesIO()
                    image.save(buffer, format="PNG")
                    buffer.seek(0)
                    st.success(f"Converted to PNG!")
                    st.download_button("Download PNG", data=buffer, file_name=converted_file)
            elif convert_to == "PDF":
                converted_file = f"{uploaded_file.name[:-4]}.pdf"
                if st.button("Convert to PDF"):
                    image = Image.open(uploaded_file)
                    image_bytes = io.BytesIO()
                    image.save(image_bytes, format='JPEG')
                    pdf_bytes = img2pdf.convert(image_bytes.getvalue())
                    st.success(f"Converted to PDF!")
                    st.download_button("Download PDF", data=pdf_bytes, file_name=converted_file)

        elif file_type == "PNG":
            # Conversion option for PNG
            convert_to = st.selectbox("Convert to:", ("JPEG",))
            if convert_to == "JPEG":
                converted_file = f"{uploaded_file.name[:-4]}.jpg"
                if st.button("Convert to JPEG"):
                    image = Image.open(uploaded_file)
                    buffer = io.BytesIO()
                    image = image.convert('RGB')
                    image.save(buffer, format="JPEG")
                    buffer.seek(0)
                    st.success(f"Converted to JPEG!")
                    st.download_button("Download JPEG", data=buffer, file_name=converted_file)

        elif file_type == "PDF":
            # Conversion option for PDF
            convert_to = st.selectbox("Convert to:", ("JPEG",))
            if convert_to == "JPEG":
                if st.button("Convert to JPEG (all pages)"):
                    with open(uploaded_file.name, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    output_dir = f"{uploaded_file.name[:-4]}_images"
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    converted_files = convert_pdf_to_jpeg(uploaded_file.name, output_dir)
                    st.success(f"Converted all pages to JPEG!")
                    for i, filename in enumerate(converted_files):
                        with open(filename, "rb") as img_file:
                            st.download_button(f"Download Page {i+1}", data=img_file.read(), file_name=os.path.basename(filename))

    st.write("*Note:* Currently, PDF to JPEG conversion saves all pages as separate images.")

if __name__ == "__main__":
    main()
