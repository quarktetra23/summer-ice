import streamlit as st
from openai import OpenAI
import PyPDF2
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

#Basic UI on Streamlit
st.set_page_config(page_title="Smart PDF Summarizer", layout="centered")
st.title("📄 Smart PDF Summarizer")
st.write("Upload a PDF file and get a concise summary using GPT!")

# Upload PDF
pdf_file = st.file_uploader("Upload your PDF file", type=["pdf"])

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


if pdf_file is not None:
    with st.spinner("Extracting text..."):
        extracted_text = extract_text_from_pdf(pdf_file)

    if extracted_text.strip():
        st.success("Text extracted successfully.")

        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                            {"role": "user", "content": f"Summarize this document:\n\n{extracted_text}"}
                        ],
                        temperature=0.5,
                        max_tokens=500
                    )

                    summary = response.choices[0].message.content
                    st.subheader("📝 Summary")
                    st.write(summary)

                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.warning("Could not extract text. Try a different PDF.")
