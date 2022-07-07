import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
import pandas as pd
import numpy as np
import glob
import os
import nltk


def error_submit():

    st.error('This is an error')
    st.stop()
# if not  nltk.find('tokenizers/punkt.zip'):
download_dir_nlkt_tokenizer=os.path.join('data','nlkt_model','punkt.zip')
if not os.path.exists(download_dir_nlkt_tokenizer):
    nltk.download('punkt',download_dir_nlkt_tokenizer)
    
st.set_page_config(layout='centered', page_icon='🎓', page_title='Diploma Generator')
st.title('🎓 Diploma PDF Generator')

st.write(
    'This app is a challenge for my girlfriend to get her birthday present'
)


st.write(
    'First challenge,'
)
first_answer_form = st.form('first_form_challenge')
first_answer = first_answer_form.text_input(
    'minimum number of walls needed in a house'
    ) 
first_answer_submit = first_answer_form.form_submit_button(
    'Are you sure that you know the answer?'
    )
if first_answer_submit:
    ###Second challenge###
    # Books from https://github.com/formcept/whiteboard
    hp_books = sorted(glob.glob(os.path.join('data','harrypotter','*.txt')))
    hp_books_name_clean={book:book.split(os.sep)[2].split('_')[0].split('.')[0] for book in hp_books}

    st.write('Here is the template we will be using:')
    book_selected=st.selectbox('Choose the correct template to solve the challenge',hp_books_name_clean)

    book_text=open(book_selected,encoding="utf-8").read()

    df = pd.DataFrame(nltk.tokenize.sent_tokenize(book_text, language='english'))

    st.dataframe(df)
    st.write('Insert the answer')
    hp_answer_form = st.form('challenge_harry_potter')
    hp_answer = hp_answer_form.text_input(
        'Only write here if you are sure about the answer, be careful'
        ) 
    hp_answer_submit = hp_answer_form.form_submit_button(
        'Are you sure that you know the answer?'
        )
    if hp_answer_submit:
        if hp_answer=='a':
            st.balloons()
            st.success('Congratulations!!!')
            
            st.write('Fill in the data:')
            name_form = st.form('name_form')
            winner = name_form.text_input('Winner name')

            name_submit = name_form.form_submit_button('Generate PDF')

            ## we generate the certificate
            if name_submit:
                env = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape())
                template = env.get_template('template.html')
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
            error_submit()
    else:
        error_submit()