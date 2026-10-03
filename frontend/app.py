import streamlit as st
import sys
import os


# --------------------------------------------------
# Connect Frontend with Backend
# --------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from backend.pdf_protector import protect_pdf


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="PDF Password Protector",
    page_icon="🔐",
    layout="centered"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #f2f2f2;
}


/* --------------------------------------------------
   Main Header
-------------------------------------------------- */

.header {
    background: linear-gradient(to right, #f5e4d0, #ef6b6b);

    padding: 30px;

    text-align: center;

    border-radius: 10px;

    margin-bottom: 30px;
}

.header-icon {
    font-size: 50px;

    margin-bottom: 8px;
}

.header-title {
    font-size: 38px;

    font-weight: bold;

    color: #111111;

    margin: 5px 0;
}

.header-subtitle {
    font-size: 18px;

    color: #222222;

    margin: 8px 0;
}


/* --------------------------------------------------
   Section Titles
-------------------------------------------------- */

.section-title {
    font-size: 24px;

    font-weight: bold;

    color: #222222;

    margin-top: 20px;

    margin-bottom: 10px;
}


/* --------------------------------------------------
   Upload Information
-------------------------------------------------- */

.upload-info {
    font-size: 14px;

    color: #666666;

    margin-top: -8px;

    margin-bottom: 15px;
}


/* --------------------------------------------------
   Privacy Notice
-------------------------------------------------- */

.privacy-box {
    background-color: #eef6ff;

    border: 1px solid #b8d9ff;

    border-radius: 10px;

    padding: 16px 18px;

    margin-top: 25px;

    margin-bottom: 20px;

    color: #174a8b;

    font-size: 14px;

    line-height: 1.6;
}

.privacy-title {
    font-size: 17px;

    font-weight: bold;

    margin-bottom: 6px;
}

.privacy-warning {
    margin-top: 8px;

    color: #8a5a00;
}


/* --------------------------------------------------
   Protect Button
-------------------------------------------------- */

div.stButton > button {

    width: 100%;

    height: 55px;

    font-size: 18px;

    font-weight: bold;

    border-radius: 8px;
}


/* --------------------------------------------------
   Download Button
-------------------------------------------------- */

div.stDownloadButton > button {

    font-size: 16px;

    font-weight: bold;

    height: 50px;

    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.html("""
<div class="header">
    <div class="header-icon">🛡️ 🔑</div>

    <div class="header-title">
        PDF Password Protector
    </div>

    <div class="header-subtitle">
        Quickly Password Protect Your PDF File
    </div>
</div>
""")

# --------------------------------------------------
# Source PDF File
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Source PDF File</div>',
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"],
    label_visibility="collapsed"
)


# PDF only information

st.html("""
<div class="upload-info">
    📄 <strong>PDF files only</strong> •
    Please upload a file with a .pdf extension
</div>
""")


# --------------------------------------------------
# Show Selected File
# --------------------------------------------------

if uploaded_file is not None:

    file_size = len(uploaded_file.getvalue()) / (1024 * 1024)

    st.info(
        f"📄 Selected file: {uploaded_file.name} "
        f"({file_size:.2f} MB)"
    )


# --------------------------------------------------
# Target PDF File
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Target PDF File</div>',
    unsafe_allow_html=True
)


target_name = st.text_input(
    "Target PDF filename",
    placeholder="Enter output filename, for example: protected_file.pdf"
)


# --------------------------------------------------
# Password
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Set User Password</div>',
    unsafe_allow_html=True
)


password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter password",
    label_visibility="collapsed"
)


# --------------------------------------------------
# Confirm Password
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Confirm Password</div>',
    unsafe_allow_html=True
)


confirm_password = st.text_input(
    "Confirm Password",
    type="password",
    placeholder="Re-enter your password",
    label_visibility="collapsed"
)


# --------------------------------------------------
# Privacy Notice
# --------------------------------------------------

st.html("""
<div class="privacy-box">

    <div class="privacy-title">
        🔒 Privacy Notice
    </div>

    <div>
        Your password is used only to protect the PDF
        and is <strong>not stored anywhere</strong> by this application.
    </div>

    <div style="margin-top: 8px;">
        The password is used only during the protection process
        and is not saved to a database, file, or account.
    </div>

    <div class="privacy-warning">
        ⚠️ If you forget the password, this application
        cannot recover or reset it.
    </div>

</div>
""")

# --------------------------------------------------
# Protect PDF Button
# --------------------------------------------------

st.write("")


if st.button("🔐 Protect PDF File"):

    # --------------------------------------------------
    # Check PDF
    # --------------------------------------------------

    if uploaded_file is None:

        st.error(
            "Please select a PDF file."
        )


    # --------------------------------------------------
    # Check Password
    # --------------------------------------------------

    elif not password:

        st.error(
            "Please enter a password."
        )


    # --------------------------------------------------
    # Check Confirm Password
    # --------------------------------------------------

    elif not confirm_password:

        st.error(
            "Please confirm your password."
        )


    # --------------------------------------------------
    # Check Password Match
    # --------------------------------------------------

    elif password != confirm_password:

        st.error(
            "The passwords do not match."
        )


    else:

        # --------------------------------------------------
        # Set Default Filename
        # --------------------------------------------------

        if not target_name.strip():

            target_name = (
                "protected_" +
                uploaded_file.name
            )


        # --------------------------------------------------
        # Make Sure Filename Ends With .pdf
        # --------------------------------------------------

        if not target_name.lower().endswith(".pdf"):

            target_name += ".pdf"


        try:

            # --------------------------------------------------
            # Read Uploaded PDF
            # --------------------------------------------------

            pdf_bytes = uploaded_file.getvalue()


            # --------------------------------------------------
            # Send PDF and Password to Backend
            # --------------------------------------------------

            protected_pdf = protect_pdf(
                pdf_bytes,
                password
            )


            # --------------------------------------------------
            # Success Message
            # --------------------------------------------------

            st.success(
                "PDF password protection completed successfully!"
            )


            # --------------------------------------------------
            # Download Protected PDF
            # --------------------------------------------------

            st.download_button(
                label="⬇️ Download Protected PDF",

                data=protected_pdf,

                file_name=target_name,

                mime="application/pdf",

                use_container_width=True
            )


        except Exception as e:

            st.error(
                f"Error while protecting PDF: {e}"
            )