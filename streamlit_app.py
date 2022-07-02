import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
import pandas as pd
import numpy as np
st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
st.title("🎓 Diploma PDF Generator")

st.write(
    "This app is a challenge for my girlfriend to get her birthday present"
)

# left, right = st.columns(2)


df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))
st.write("Here's the template we'll be using:")
st.selectbox('Elige la plantilla correcta para resolver el challenge',['a','b','c','d'])
st.dataframe(df)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")


st.write("Fill in the data:")
form = st.form("template_form")
winner = form.text_input("Winner name")
# course = form.selectbox(
#     "Choose course",
#     ["Report Generation in Streamlit", "Advanced Cryptography"],
#     index=0,
# )
# grade = form.slider("Grade", 1, 100, 60)
submit = form.form_submit_button("Generate PDF")

# submit=True

# winner='BEGO'

## we generate the certificate
if submit:
    html = template.render(
        winner=winner,
        date=date.today().strftime("%B %d, %Y"),
    )
    path_wkhtmltopdf = r'D:\programacion\Repositorios\bego_challenge_2022\whkhtml\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf,)
    pdf = pdfkit.from_string(html, False,configuration=config)
    st.balloons()

    st.success("🎉 Your diploma was generated!")
    # st.write(html, unsafe_allow_html=True)
    # st.write("")
    st.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name="diploma.pdf",
        mime="application/octet-stream",
    )
