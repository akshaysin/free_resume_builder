# Free Resume Builder

Welcome to our free, open-source resume-building platform! This project empowers anyone to create professional resumes quickly and easily, with no cost or sign-up required.

## Features
- **Modern Templates:** Choose from "Simple and Moderne" or "Executive" resume templates.
- **Dynamic Form:** Add/remove jobs, education, certifications, and skills interactively.
- **Image Upload:** Upload a profile picture (under 60 KB) or use a URL.
- **Sidebar Skills:** For the executive template, skills are managed in the sidebar.
- **Download Options:** Download your resume as HTML or JSON (PDF can be generated from HTML using your browser).
- **About Page:** Learn about the project and contact the author for feedback.

## How to Use
1. **Clone this repository** and install dependencies:
   ```bash
   git clone <your-repo-url>
   cd resumeV2
   pip install -r requirements.txt
   ```
2. **Run the app:**
   ```bash
   streamlit run app.py
   ```
3. **Build your resume:**
   - Fill in your personal info, experience, education, certifications, and skills.
   - Upload a profile picture if desired.
   - Click "Generate Resume" and download as HTML or JSON.
   - For PDF, open the HTML in your browser and use "Print to PDF".

## Deployment
- **Streamlit Community Cloud:**
  - Push your code to a public GitHub repository.
  - Deploy for free at [streamlit.io/cloud](https://streamlit.io/cloud).
- **Other options:** PythonAnywhere, Render, Railway, Fly.io (see their docs for details).

## Limitations
- PDF generation is not available on Streamlit Community Cloud due to system library restrictions. Use browser print-to-PDF instead.
- SEO is limited due to Streamlit's architecture.

## Feedback & Contact
Your feedback is invaluable! Please reach out to [akshaysin@gmail.com](mailto:akshaysin@gmail.com) with suggestions or questions.

---

**Always free. Always open source. Empower your career!**
