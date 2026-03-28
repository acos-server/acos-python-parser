import requests
from io import BytesIO
import streamlit as st
from streamlit_ace import st_ace
from concepts_parser import main, post_process_parser
import os
import pandas as pd

# option = st.selectbox("Select Programming Language",("python","java"))

pitt_url = 'https://www.pitt.edu/sites/default/files/assets/pitt_shield_white-home.png'
img_a = requests.get(pitt_url)
pitt_img = BytesIO(img_a.content).read()

url = 'http://adapt2.sis.pitt.edu/w/images/1/19/PAWS_logo.png'
img_b = requests.get(url)
favicon = BytesIO(img_b.content).read()

st.set_page_config(page_title="PCCP",
                   page_icon=favicon)
st.image(pitt_img,output_format='png')
st.image(favicon,output_format='png')

st.title("Python Code Concepts Parser")

code_string = """
### enter code here

""" \
# if option == 'python' else \
# """
# // enter code here
# """

with st.form("code_form"):
    
    code = st_ace(value=code_string,
                language="python",
                min_lines= 50,
                max_lines=500,
                auto_update=True,
                theme="dracula")
                
    content_name = st.text_input(label='Please Provide Aggregate2 Content Name:',placeholder='tmp1',value='tmp1',key='kc_content_component_name', disabled = not code)
    activity_id = st.text_input(label='Please Provide um2 Activity Id:', key='um2_activity_id', placeholder='111111',value='111111',disabled = not code) 

    submitted = st.form_submit_button("Submit Code")

    if submitted:
        if not(os.path.exists('./py-files')): os.mkdir('py-files')
        with open(f'./py-files/tmp1.py','w+') as f:
            f.write(code)

        response = main(filename='py-files/tmp1.py')
        smart_concepts_sections = pd.DataFrame.from_records(post_process_parser(response,content_name,activity_id))
        st.dataframe(smart_concepts_sections)

        os.remove('./py-files/tmp1.py')
        os.rmdir('./py-files')
