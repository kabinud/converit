import streamlit as st
import base64
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

def get_base64_encoded_image(image_data):
    return base64.b64encode(image_data).decode()

def pdf_to_image(bytes_data):
    with fitz.open(stream=bytes_data, filetype="pdf") as doc:
        page = doc.load_page(0)  # loading the first page
        pix = page.get_pixmap()
        img = Image.open(BytesIO(pix.tobytes("ppm")))
        return img

def main():
    st.title('Image/PDF to Base64 Encoder')

    uploaded_file = st.file_uploader("Choose a file (JPG, PNG, PDF, up to 2MB)", type=["jpg", "png", "pdf"])
    
    if uploaded_file is not None:
        file_size = uploaded_file.size
        bytes_data = uploaded_file.getvalue()

        # File size limit (2MB)
        file_size_limit = 2 * 1024 * 1024  # 2 MB in bytes

        if file_size > file_size_limit:
            st.error("Oops - The file size exceeds the 2MB limit.")
            return

        # Create two columns for the preview and the base64 output
        col1, col2 = st.columns(2)

        with col1:
            st.write("Preview:")
            if uploaded_file.type in ["image/jpeg", "image/png"]:
                st.image(bytes_data, caption="Uploaded Image", use_column_width=True)
            elif uploaded_file.type == "application/pdf":
                with st.spinner('Processing PDF...'):
                    try:
                        preview_image = pdf_to_image(bytes_data)
                        st.image(preview_image, caption="PDF First Page Preview", use_column_width=True)
                    except Exception as e:
                        st.error("Could not load PDF preview: {}".format(e))

        with col2:
            st.write("Base64 Encoded Output:")
            with st.spinner('Encoding...'):
                base64_encoded_result = get_base64_encoded_image(bytes_data)
                st.text_area("", base64_encoded_result, height=400, key="base64_output")
            
            copy_btn = st.button('Copy to Clipboard', key='copy_base64')
            
            if copy_btn:
                st.warning('Please manually copy the text above. Direct copy to clipboard is not supported.')

        st.markdown('**Note:** Direct copying to clipboard is not supported due to browser security restrictions. Please manually copy the base64 encoded output.')

if __name__ == "__main__":
    main()
