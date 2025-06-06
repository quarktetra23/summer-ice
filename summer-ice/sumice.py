import streamlit as st
import PyPDF2
from pdf_summary import summarize_text
from image_generator import generate_image

# UI
st.set_page_config(page_title="Summer-Ice", layout="centered")
st.title("📄 PDF Summarize & 🎨 Image Generation")

# Upload PDF
pdf_file = st.file_uploader("Upload your PDF file", type=["pdf"])

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

mode = st.radio("Operations to perform", ("Summarize", "Generate Image"))

# if the pdf is uploaded
if pdf_file is not None:
    with st.spinner("Extracting text..."):
        extracted_text = extract_text_from_pdf(pdf_file)

    # and the text is extracted
    if extracted_text.strip():
        st.success("Text extracted successfully.")

        # PDF Summarize 
        if mode == "Summarize":
            if st.button("Summarize"):
                with st.spinner("Summarizing..."):
                    try:
                        summary = summarize_text(extracted_text)
                        st.subheader("📝 Summary")
                        st.write(summary)
                    except Exception as e:
                        st.error(f"Error summarizing: {str(e)}")

        # Image Generation mode
        elif mode == "Generate Image":
            # Optional: User can override image prompt
            custom_prompt = st.text_input("Optional: Enter a custom image prompt (otherwise PDF text will be used)")

            if st.button("Generate Image"):
                with st.spinner("Generating image..."):
                    try:
                        final_prompt = custom_prompt if custom_prompt.strip() else f"Create an artistic illustration representing the following document content:\n\n{extracted_text[:1000]}"
                        image_url = generate_image(final_prompt)
                        st.subheader("🎨 Generated Image")
                        st.image(image_url, use_column_width=True)
                    except Exception as e:
                        st.error(f"Error generating image: {str(e)}")
    else:
        st.warning("Could not extract text. Try a different PDF.")

else:
    st.info("Please upload a PDF file to begin.")
