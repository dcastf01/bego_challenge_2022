import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
import pandas as pd
import numpy as np
import glob
import os
st.set_page_config(layout='centered', page_icon='🎓', page_title='Diploma Generator')
st.title('🎓 Diploma PDF Generator')

st.write(
    'This app is a challenge for my girlfriend to get her birthday present'
)

# left, right = st.columns(2)

# Books present
books = sorted(glob.glob(os.path.join('data','harrypotter','*.txt')))

print ('Available Books: \n')
for i in books:
    print (i.split(os.sep)[2].split('_')[0].split('.')[0])


df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))
st.write('Here is the template we will be using:')
st.selectbox('Choose the correct template to solve the challenge',['a','b','c','d'])
st.dataframe(df)

env = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape())
template = env.get_template('template.html')

st.write('Insert the answer')
answer_form = st.form('template_form')
answer = answer_form.text_input(
    'Only write here if you are sure about the answer, be careful'
    ) 
answer_submit = answer_form.form_submit_button(
    'Are you sure that you know the answer?'
    )
if answer_submit:
    if answer=='a':
        st.balloons()
        st.success('Congratulations!!!')
        
        st.write('Fill in the data:')
        name_form = st.form('name_form')
        winner = name_form.text_input('Winner name')

        name_submit = name_form.form_submit_button('Generate PDF')

        # submit=True

        # winner='BEGO'

        ## we generate the certificate
        if name_submit:
            html = template.render(
                winner=winner,
                date=date.today().strftime('%B %d, %Y'),
            )
            path_wkhtmltopdf=os.path.join(
                'whkhtml','wkhtmltopdf','bin','wkhtmltopdf.exe'
                )
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf,)
            pdf = pdfkit.from_string(html, False,configuration=config)
            st.balloons()

            st.success('🎉 Your diploma was generated!')
            # st.write(html, unsafe_allow_html=True)
            # st.write('')
            st.download_button(
                '⬇️ Download PDF',
                data=pdf,
                file_name='diploma.pdf',
                mime='application/octet-stream',
            )

    else:
        st.error('This is an error')
        st.stop()