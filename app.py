import streamlit as st
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import io
import tempfile


def main():
    # Set page configuration
    st.set_page_config(page_title='Pasting Made Easy 🚀🚀', page_icon='💼', layout='centered',
                       initial_sidebar_state='collapsed')

    # Apply custom CSS for aesthetic changes
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(to right, #6528F7, #B2A4FF),
                            radial-gradient(circle, #D7BBF5, #EDE4FF); /* Gradient background */
            }
            body {
                color: #000000; /* Dark gray text */
                font-size: 18px;
            }
            .stButton>button {
                background-color: #200E3A; /* Blue button */
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #0056b3; 
            }
            .footer {
                position: fixed;
                bottom: 10px;
                left: 50%;
                transform: translateX(-50%);
                color: #030637; 
                font-size: 14px;
            }
            .dialogue-box {
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0px 8px 12px rgba(0.4, 0, 0, 0.7);
            }
            .happy-editing {
                position: absolute;
                bottom: 10px;
                right: 10px;
                color: #030637;
                font-size: 14px;
            }
            .file-upload-label {
                background-color: #200E3A;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                padding: 10px 20px;
                cursor: pointer;
            }
            .file-upload-input {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
  

    st.title('Pasting Made Easy 🚀🚀')

    # Dialogue box
    st.markdown(
        """
        <div class="dialogue-box">
            Upload the formatted PDF you wish to see your letterhead on!!<br/>
            Upload your desired image! and you're good to go
        </div>
        """,
        unsafe_allow_html=True
    )

    pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])
    image_file = st.file_uploader("Upload Image File", type=["jpg", "png"])

    if st.button("Initiate Job 💼"):
        if pdf_file and image_file:
            processed_pdf = add_image_to_pdf(pdf_file, image_file)
            st.download_button("Download Processed PDF", processed_pdf, file_name="output.pdf", key="download-btn")

    # Footer
    st.markdown('<div class="footer">Created by 😎Soham</div>', unsafe_allow_html=True)

    # Happy Editing message
    st.markdown('<div class="happy-editing">Happy Editing! 😊</div>', unsafe_allow_html=True)


def add_image_to_pdf(pdf_file, image_file):
    pdf_reader = PdfFileReader(pdf_file)
    pdf_writer = PdfFileWriter()

    image = Image.open(image_file)
    new_width = letter[0]
    new_height = (new_width / image.width) * image.height

    temp_image_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    resized_image = image.resize((int(new_width), int(new_height)))
    resized_image.save(temp_image_path.name)

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.getPage(page_number)

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        y_coordinate = letter[1] - new_height

        can.drawImage(temp_image_path.name, 0, y_coordinate, width=new_width, height=new_height)
        can.showPage()
        can.save()

        packet.seek(0)
        overlay_reader = PdfFileReader(packet)
        overlay_page = overlay_reader.getPage(0)  # Use getPage instead of pages[0]

        page.mergePage(overlay_page)

        pdf_writer.addPage(page)  # Corrected this line to use addPage

    output_pdf = io.BytesIO()
    pdf_writer.write(output_pdf)

    return output_pdf.getvalue()

if __name__ == '__main__':
    main()
