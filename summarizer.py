elif feature == lang["summarizer"]:

    st.header("🧠 AI Notes Summarizer")

    st.write("""
Upload PDF notes or paste text manually
to generate AI-powered summaries.
""")

    # PDF Upload
    uploaded_file = st.file_uploader(
        "📄 Upload PDF Notes",
        type=["pdf"]
    )

    text = ""

    # Extract text from PDF
    if uploaded_file:

        from PyPDF2 import PdfReader

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            extracted_text = page.extract_text()

            if extracted_text:
                text += extracted_text

        st.success("✅ PDF Uploaded Successfully")

    # Manual Text Area
    text_input = st.text_area(
        "Or Paste Notes Here",
        height=300
    )

    # Combine PDF text + manual text
    if text_input:
        text += text_input

    summary_length = st.selectbox(
        "Select Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    if st.button(lang["summary_button"]):

        if text:

            sentences = text.split('.')

            if summary_length == "Short":
                summary = '.'.join(sentences[:2])

            elif summary_length == "Medium":
                summary = '.'.join(sentences[:4])

            else:
                summary = '.'.join(sentences[:7])

            st.success("✅ Summary Generated Successfully")

            st.subheader("📄 Generated Summary")

            st.write(summary)

            st.info(f"📊 Total Word Count: {len(text.split())}")

        else:
            st.warning("⚠️ Please upload PDF or enter notes.")
