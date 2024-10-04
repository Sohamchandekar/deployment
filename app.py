import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
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

        # Text input for alphanumeric string
        udin_text = st.text_input("Enter the Alphanumeric UDIN Number")

        # Slider for top margin
        top_margin = st.slider("Select Top Margin (in pixels)", min_value=0, max_value=100, value=0)

        # Dropdown for selecting the format (Old or New)
        format_type = st.selectbox("Select Form3 Format", ["Old Format", "New Format"])

    if st.button("Initiate Job 💼"):
        if pdf_file and udin_text:
            # Extract the 2nd to 7th characters to determine the letterhead
            udin_substring = udin_text[2:8]
            if udin_substring == "188808":
                letterhead_file = "letterhead/RNA.png"
            elif udin_substring == "627790":
                letterhead_file = "letterhead/PTA.png"
            elif udin_substring == "631662":
                letterhead_file = "letterhead/NSA.png"
            else:
                st.error("The UDIN does not match any known letterhead. Please check the number.")
                return

            # Call the appropriate function based on format selection
            if format_type == "Old Format":
                processed_pdf = add_letterhead_to_pdf_old(pdf_file, letterhead_file, top_margin)
            else:
                processed_pdf = add_letterhead_to_pdf_new(pdf_file, letterhead_file, top_margin)

            st.download_button("Download Processed PDF", processed_pdf, file_name="output.pdf", key="download-btn")
    # Footer
    st.markdown('<div class="footer">Created by 😎Soham</div>', unsafe_allow_html=True)

    # Happy Editing message
    st.markdown('<div class="happy-editing">Happy Editing! 😊</div>', unsafe_allow_html=True)

def add_letterhead_to_pdf_new(main_pdf_file, letterhead_image_file, top_margin):
    # Read the main PDF
    main_pdf_reader = PdfReader(main_pdf_file)
    pdf_writer = PdfWriter()

    # Set A4 paper size dimensions (in points)
    a4_width, a4_height = A4  # This gives dimensions in points (1 inch = 72 points)

    # Open the letterhead image and get its dimensions
    img = Image.open(letterhead_image_file)
    img_width, img_height = img.size

    # Calculate the aspect ratio of the image
    aspect_ratio = img_width / img_height

    # Calculate the letterhead's display width and height, keeping the width equal to the A4 page width
    width = a4_width  # Fit the letterhead to the full width of the A4 page
    height = width / aspect_ratio

    # Create a temporary PDF for the letterhead
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # Draw the image at the top of the first page, accounting for the top margin
    can.drawImage(letterhead_image_file, 0, a4_height - height - top_margin, width=width, height=height)

    can.save()
    packet.seek(0)

    # Read the overlay with the letterhead
    overlay_reader = PdfReader(packet)
    overlay_page = overlay_reader.pages[0]

    # Get the first page of the main PDF and merge the letterhead
    first_page = main_pdf_reader.pages[0]
    first_page.merge_page(overlay_page)
    pdf_writer.add_page(first_page)

    # Add the rest of the pages without any letterhead overlay
    for page_number in range(1, len(main_pdf_reader.pages)):
        pdf_writer.add_page(main_pdf_reader.pages[page_number])

    # Save the new PDF with the letterhead only on the first page
    output_pdf = io.BytesIO()
    pdf_writer.write(output_pdf)
    output_pdf.seek(0)

    return output_pdf.getvalue()


def add_letterhead_to_pdf_old(main_pdf_file, letterhead_image_file, top_margin):
    main_pdf_reader = PdfReader(main_pdf_file)
    pdf_writer = PdfWriter()

    # Open the image and get its dimensions
    img = Image.open(letterhead_image_file)
    img_width, img_height = img.size

    # Calculate the aspect ratio
    aspect_ratio = img_width / img_height

    # Calculate the width and height based on the aspect ratio
    width = letter[0]
    height = width / aspect_ratio

    # Create a temporary PDF for the letterhead top part
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Draw the image at the top of the page with margin
    can.drawImage(letterhead_image_file, 0, letter[1] - height - top_margin, width=width, height=height)

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
