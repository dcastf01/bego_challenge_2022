from ast import With
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
from PIL import Image

def error_submit():

    st.error('This is an error')
    st.stop()
# if not  nltk.find('tokenizers/punkt.zip'):
download_dir_nlkt_tokenizer=os.path.join('data','nlkt_model','punkt.zip')
if not os.path.exists(download_dir_nlkt_tokenizer):
    nltk.download('punkt',download_dir_nlkt_tokenizer)
    
st.set_page_config(layout='centered', page_icon='💖', page_title='Diploma Generator')
st.title('💖 Voucher gift PDF Generator')

st.write(
    'This app is a challenge for my girlfriend to get her birthday present'
)
st.subheader('Challenges!!')
col1, col2, col3 = st.columns(3)
with col1:
    st.write('First challenge: book')
    list_of_options_first=range(0,5)
    option_first = st.selectbox(
        'minimum number of walls needed in a room',
        ('choose wisely',*list_of_options_first))
    
    if option_first != 'choose wisely':
        if option_first!=1:
            error_submit()
        else:
            st.write('Well Done')
            image_path=os.path.join('data','assets','circular room.jpg')
            image = Image.open(image_path)

            st.image(image, caption="to prove it's true")
            st.markdown('*5*')
with col2:
    st.write(
        'Second challenge: line'
    )
    list_of_options_second=[
        'Thestral',
        'Acromántula',
        'Horned Serpent',
        'Basilisk',
        'Sorting hat',
        'Centaur',
        'Chimaera',
        ]
    option_second = st.selectbox(
       """Year after year
        the students are testing me
        and i told them
        in which house will they be studying""",
        ('choose wisely',*list_of_options_second))

    if option_second != 'choose wisely':
        if option_second!='Sorting hat':
            error_submit()
        else:
            st.write('Well Done')
           
            st.markdown('*2527*')

with col3:
    st.write(
        'Third challenge: word'
    )

    image_path=os.path.join('data','assets','bleach.png')
    image = Image.open(image_path)

    st.image(image, caption="to prove it's true")
    list_of_options_third=[
        'Naruto',
        'Naruto: Shippuden'
        'Full Metal Alchemist',
        'My Hero Academia',
        'One Piece',
        'Sword Art Online',
        'Kimetsu No Yaiba',
        'Shaman king',
        'Haikyu',
        'shingeky no Kyojin',
        'Bleach',
        'Fairy Tail',
        'Nanatsu No Taizai',
        ]
    option_third = st.selectbox(
       'From which anime is the image?',
        ('choose wisely',*list_of_options_third))

    if option_third != 'choose wisely':
        if option_third!='Bleach':
            error_submit()
        else:
            st.write('Well Done')
           
            st.markdown('*10*') 

###Second challenge###
# Books from https://github.com/formcept/whiteboard
hp_books = sorted(glob.glob(os.path.join('data','harrypotter','*.txt')))
hp_books_name_clean={book.split(os.sep)[2].split('_')[0].split('.')[0]:book for book in hp_books}

st.write('Here is the template we will be using:')
book_selected=st.selectbox('Choose the correct template to solve the challenge',hp_books_name_clean.keys())

book_text=open(hp_books_name_clean[book_selected],encoding="utf-8").read()

df = pd.DataFrame(nltk.tokenize.sent_tokenize(book_text, language='english'))
df.rename({0:'sentences'},inplace=True,axis=1)

sentences_to_show=st.number_input('do you know what is the sentences?',min_value=0,max_value=df.shape[0])
if sentences_to_show:
    st.dataframe(df.iloc[sentences_to_show])
else:
    st.dataframe(df)
st.write('Insert here the final key to unlock the prize')
challenge_harry_potter_form = st.form('challenge_harry_potter_form')
hp_answer = challenge_harry_potter_form.text_input(
    'Only write here if you are sure about the answer, be careful'
    ) 
hp_answer_submit = challenge_harry_potter_form.form_submit_button(
    'Are you sure that you know the answer? testing'
    )

#hacer que escriba la plabra alohomora para ello tiene que encontrarla en el libro 5  sentences 2527 y palabra 10
#para ello tengo que pner ciertas pistas, donde una es libro, otra la frase y la otra el numero de la palbra
# quizá las preguntas son con sumas o cosas varias
if hp_answer_submit:
    if hp_answer=='Alohomora':
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
