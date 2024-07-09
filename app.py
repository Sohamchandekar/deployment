import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from PIL import Image

def main():
    # Set page configuration
    st.set_page_config(page_title='LetterHead Pasting Tool 🚀🚀', page_icon='💼', layout='wide',
                       initial_sidebar_state='collapsed')

    # Apply custom CSS for aesthetic changes
    st.markdown(
        """
        <style>
        
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
            .stApp {
                background: linear-gradient(to right, #6528F7, #B2A4FF),
                            radial-gradient(circle, #D7BBF5, #EDE4FF); /* Gradient background */
                            font-family: 'Roboto Mono', monospace; /* Change font */
            }
            body {
                color: #000000; /* Dark gray text */
                font-family: 'Roboto Mono', monospace; /* Change font */
                font-size: 18px;
            }
            .stButton>button {
                background-color: #200E3A; /* Blue button */
                font-family: 'Roboto Mono', monospace; /* Change font */
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
                font-family: 'Roboto Mono', monospace; /* Change font */
                bottom: 10px;
                left: 50%;
                transform: translateX(-50%);
                color: #030637; 
                font-size: 14px;
            }
            .dialogue-box {
                padding: 20px;
                font-family: 'Roboto Mono', monospace; /* Change font */
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0px 8px 12px rgba(0.4, 0, 0, 0.7);
            }
            .happy-editing {
                position: absolute;
                font-family: 'Roboto Mono', monospace; /* Change font */
                bottom: 10px;
                right: 10px;
                color: #030637;
                font-size: 14px;
            }
            .file-upload-label {
                background-color: #200E3A;
                font-family: 'Roboto Mono', monospace; /* Change font */
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

    quote = """
    <div style='font-style: italic; font-weight: bold; font-size: 15px; color: #222222; border-left: 3.5px solid gray; padding-left: 10px; margin-bottom: 10px;'>
        💡"Lamba Saans le aur dimag mein oxygen bhar, <br> kyunki dimag mein rahegi shanti tabhi aayegi Kranti" <br> -Jackie Shroff🌳
    </div>
    """
    st.markdown(quote, unsafe_allow_html=True)
    st.title('Pasting Made Easy 🚀🚀')

    col1, col2 = st.columns([1, 2])

    with col1:
        # Dialogue box
        st.markdown(
            """
            <div class="dialogue-box">
                Upload the formatted PDF you wish to see your letterhead on!!<br/>
                Select your desired letterhead dropdown and you're good to go
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # File uploader for main PDF
        pdf_file = st.file_uploader("Upload PDF File", type=["pdf"], key="pdf-uploader")

        # Dropdown for letterhead selection
        letterhead_option = st.selectbox(
            "Select Letterhead",
            ("Rutuja Narsingh & Associates", "Pratiksha Tulshyan & Associates")
        )

    if st.button("Initiate Job 💼"):
        if pdf_file and letterhead_option:
            letterhead_file = "letterhead/RNA.png" if letterhead_option == "Rutuja Narsingh & Associates" else "letterhead/PTA.png"
            processed_pdf = add_letterhead_to_pdf(pdf_file, letterhead_file)
            st.download_button("Download Processed PDF", processed_pdf, file_name="output.pdf", key="download-btn")

    # Footer
    st.markdown('<div class="footer">Created by 😎Soham</div>', unsafe_allow_html=True)

    # Happy Editing message
    st.markdown('<div class="happy-editing">Happy Editing! 😊</div>', unsafe_allow_html=True)


def add_letterhead_to_pdf(main_pdf_file, letterhead_image_file):
    main_pdf_reader = PdfReader(main_pdf_file)
    pdf_writer = PdfWriter()

    # Create a temporary PDF for the letterhead top part
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Draw the image at the top of the page
    can.drawImage(letterhead_image_file, 0, letter[1] - 100, width=letter[0], height=105)

    can.showPage()
    can.save()
    packet.seek(0)
    overlay_reader = PdfReader(packet)
    overlay_page = overlay_reader.pages[0]

    for page_number in range(len(main_pdf_reader.pages)):
        page = main_pdf_reader.pages[page_number]
        page.merge_page(overlay_page)
        pdf_writer.add_page(page)

    output_pdf = io.BytesIO()
    pdf_writer.write(output_pdf)

    return output_pdf.getvalue()

if __name__ == '__main__':
    main()
