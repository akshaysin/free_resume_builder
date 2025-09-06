import streamlit as st
import os
import jinja2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def get_templates():
    return [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.html')]

def render_resume(template_name, context):
    with open(os.path.join(TEMPLATE_DIR, template_name), 'r', encoding='utf-8') as f:
        template_str = f.read()
    template = jinja2.Template(template_str)
    return template.render(**context)

def main():
    st.set_page_config(page_title='Resume Builder', page_icon=':briefcase:')
    menu = ["Resume Builder", "About"]
    choice = st.sidebar.selectbox("Navigation", menu)
    if choice == "About":
        st.title('About This Project')
        st.markdown('''
Welcome to our free resume-building platform! I’m passionate about empowering individuals to create professional resumes effortlessly. This service allows users to generate and download their resumes in HTML or JSON format, which can be easily converted to PDF for sharing. Best of all, it’s always free! Your feedback is invaluable—feel free to reach out at [akshaysin@gmail.com](mailto:akshaysin@gmail.com) to share your thoughts or suggestions.
        ''')
        return
    st.title('Resume Builder')
    templates = get_templates()
    template_labels = {
        'simple_modern.html': 'Simple and Moderne',
        'executive.html': 'Executive',
    }
    template_options = [template_labels.get(t, t) for t in templates]
    template_choice = st.selectbox('Choose a template', template_options)
    # Map back to filename
    template_name = templates[template_options.index(template_choice)]

    # --- Personal Info ---
    st.header('Personal Information')
    name = st.text_input('Full Name')
    email = st.text_input('Email')
    phone = st.text_input('Phone')
    address = st.text_input('Address')
    summary = st.text_area('Summary')
    headline = st.text_input('Headline')
    website = st.text_input('Website URL')
    col_pic1, col_pic2 = st.columns([2,1])
    with col_pic1:
        picture_url = st.text_input('Picture URL', value='https://i.imgur.com/HgwyOuJ.jpg', key='picture_url')
    with col_pic2:
        uploaded_img = st.file_uploader('Upload Image (<60 KB)', type=['jpg', 'jpeg', 'png'], key='picture_upload')
        if uploaded_img is not None:
            if uploaded_img.size > 60 * 1024:
                st.warning('Image must be less than 60 KB.')
            else:
                import base64
                img_bytes = uploaded_img.read()
                img_b64 = base64.b64encode(img_bytes).decode('utf-8')
                mime = uploaded_img.type
                picture_url = f'data:{mime};base64,{img_b64}'

    # --- Experience (Dynamic) ---
    st.header('Experience')
    if 'jobs' not in st.session_state:
        st.session_state['jobs'] = []
    if st.button('Add Job'):
        st.session_state['jobs'].append({
            'position': '', 'company': '', 'location': '', 'start_date': None, 'end_date': None, 'currently_working': False, 'description': ''
        })
    jobs_to_remove = []
    for idx, job in enumerate(st.session_state['jobs']):
        with st.expander(f'Job #{idx+1}'):
            job['position'] = st.text_input(f'Position', value=job['position'], key=f'pos_{idx}')
            job['company'] = st.text_input(f'Company', value=job['company'], key=f'comp_{idx}')
            job['location'] = st.text_input(f'Location', value=job['location'], key=f'loc_{idx}')
            job['start_date'] = st.date_input(f'Start Date', value=job['start_date'] or None, key=f'start_{idx}')
            job['currently_working'] = st.checkbox('Currently working here', value=job['currently_working'], key=f'curr_{idx}')
            if not job['currently_working']:
                job['end_date'] = st.date_input(f'End Date', value=job['end_date'] or None, key=f'end_{idx}')
            else:
                job['end_date'] = None
            job['description'] = st.text_area('Description', value=job['description'], key=f'desc_{idx}')
            if st.button('Remove Job', key=f'remove_job_{idx}'):
                jobs_to_remove.append(idx)
    for idx in reversed(jobs_to_remove):
        st.session_state['jobs'].pop(idx)

    # --- Education (Dynamic) ---
    st.header('Education')
    if 'education' not in st.session_state:
        st.session_state['education'] = []
    if st.button('Add Education'):
        st.session_state['education'].append({
            'degree': '', 'school': '', 'area': '', 'start_date': None, 'end_date': None
        })
    edu_to_remove = []
    for idx, edu in enumerate(st.session_state['education']):
        with st.expander(f'Education #{idx+1}'):
            edu['degree'] = st.text_input('Degree', value=edu['degree'], key=f'deg_{idx}')
            edu['school'] = st.text_input('School', value=edu['school'], key=f'school_{idx}')
            edu['area'] = st.text_input('Field of Study', value=edu['area'], key=f'area_{idx}')
            edu['start_date'] = st.date_input('Start Date', value=edu['start_date'] or None, key=f'edustart_{idx}')
            edu['end_date'] = st.date_input('End Date', value=edu['end_date'] or None, key=f'eduend_{idx}')
            if st.button('Remove Education', key=f'remove_edu_{idx}'):
                edu_to_remove.append(idx)
    for idx in reversed(edu_to_remove):
        st.session_state['education'].pop(idx)

    # --- Certifications (Dynamic) ---
    st.header('Certifications')
    if 'certifications' not in st.session_state:
        st.session_state['certifications'] = []
    if st.button('Add Certification'):
        st.session_state['certifications'].append({'name': '', 'issuer': '', 'date': None})
    certs_to_remove = []
    for idx, cert in enumerate(st.session_state['certifications']):
        with st.expander(f'Certification #{idx+1}'):
            cert['name'] = st.text_input('Certification Name', value=cert['name'], key=f'cert_name_{idx}')
            cert['issuer'] = st.text_input('Issuer', value=cert['issuer'], key=f'cert_issuer_{idx}')
            cert['date'] = st.date_input('Date', value=cert['date'] or None, key=f'cert_date_{idx}')
            if st.button('Remove Certification', key=f'remove_cert_{idx}'):
                certs_to_remove.append(idx)
    for idx in reversed(certs_to_remove):
        st.session_state['certifications'].pop(idx)

    # --- Skills in Sidebar ---
    if template_name == 'executive.html':
        with st.sidebar:
            st.header('Skills (Executive)')
            if 'skills_exec' not in st.session_state:
                st.session_state['skills_exec'] = []
            if st.button('Add Skill', key='add_skill'):
                st.session_state['skills_exec'].append({'name': '', 'keywords': []})
            skills_to_remove = []
            for idx, skill in enumerate(st.session_state['skills_exec']):
                with st.expander(f'Skill #{idx+1}', expanded=True):
                    skill['name'] = st.text_input('Skill Name', value=skill['name'], key=f'skill_name_{idx}')
                    keywords_str = st.text_area('Keywords (comma separated)', value=','.join(skill['keywords']), key=f'skill_keywords_{idx}')
                    skill['keywords'] = [k.strip() for k in keywords_str.split(',') if k.strip()]
                    if st.button('Remove Skill', key=f'remove_skill_{idx}'):
                        skills_to_remove.append(idx)
            for idx in reversed(skills_to_remove):
                st.session_state['skills_exec'].pop(idx)

    # --- Context Construction ---
    if template_name == 'executive.html':
        context = {
            'basics': {
                'name': name,
                'headline': headline,
                'email': email,
                'phone': phone,
                'location': address,
                'url': {'label': '', 'href': website},
                'customFields': [],
                'picture': {
                    'url': picture_url,
                    'size': 120,
                    'aspectRatio': 1.2,
                    'borderRadius': 4,
                    'effects': {'hidden': False, 'border': False, 'grayscale': False}
                }
            },
            'sections': {
                'summary': {
                    'name': 'Summary',
                    'columns': 1,
                    'visible': True,
                    'id': 'summary',
                    'content': summary
                },
                'experience': {
                    'name': 'Experience',
                    'columns': 1,
                    'visible': True,
                    'id': 'experience',
                    'items': [
                        {
                            'company': job['company'],
                            'position': job['position'],
                            'location': job['location'],
                            'date': f"{job['start_date']} - {'Present' if job['currently_working'] else job['end_date']}",
                            'summary': job['description'],
                            'url': {'label': '', 'href': ''}
                        } for job in st.session_state['jobs']
                    ]
                },
                'education': {
                    'name': 'Education',
                    'columns': 1,
                    'visible': True,
                    'id': 'education',
                    'items': [
                        {
                            'institution': edu['school'],
                            'studyType': edu['degree'],
                            'area': edu['area'],
                            'date': f"{edu['start_date']} - {edu['end_date']}",
                            'summary': '',
                            'url': {'label': '', 'href': ''}
                        } for edu in st.session_state['education']
                    ]
                },
                'skills': {
                    'name': 'Skills',
                    'columns': 1,
                    'visible': True,
                    'id': 'skills',
                    'items': st.session_state.get('skills_exec', [])
                },
                'certifications': {
                    'name': 'Certifications',
                    'columns': 1,
                    'visible': True,
                    'id': 'certifications',
                    'items': [
                        {
                            'name': cert['name'],
                            'issuer': cert['issuer'],
                            'date': cert['date']
                        } for cert in st.session_state['certifications']
                    ]
                },
                'profiles': {
                    'name': 'Profiles',
                    'columns': 1,
                    'visible': True,
                    'id': 'profiles',
                    'items': []
                }
            }
        }
    else:
        with st.sidebar:
            skills = st.text_area('List your skills (comma separated)').split(',')
            skills = [s.strip() for s in skills if s.strip()]
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'summary': summary,
            'experience': st.session_state['jobs'],
            'education': st.session_state['education'],
            'skills': skills,
        }

    import json
    # Use columns to align buttons horizontally
    col1, col2 = st.columns([1, 1])
    with col1:
        generate_clicked = st.button('Generate Resume')
    with col2:
        # Placeholder for download button, will be enabled after generation
        download_json_placeholder = st.empty()
        download_html_placeholder = st.empty()

    if 'resume_html' not in st.session_state:
        st.session_state['resume_html'] = ''
    if 'resume_context' not in st.session_state:
        st.session_state['resume_context'] = None

    if generate_clicked:
        html = render_resume(template_name, context)
        st.session_state['resume_html'] = html
        st.session_state['resume_context'] = context
        st.markdown('### Preview', unsafe_allow_html=True)
        st.components.v1.html(html, height=900, scrolling=True)

    # Show preview and download buttons if resume is generated
    if st.session_state['resume_html']:
        st.markdown('### Preview', unsafe_allow_html=True)
        st.components.v1.html(st.session_state['resume_html'], height=900, scrolling=True)
        with col2:
            download_json_placeholder.download_button(
                'Download as JSON',
                data=json.dumps(st.session_state['resume_context'], indent=2),
                file_name='resume.json',
                mime='application/json'
            )
            download_html_placeholder.download_button(
                'Download as HTML',
                data=st.session_state['resume_html'],
                file_name='resume.html',
                mime='text/html'
            )

if __name__ == '__main__':
    main()
