import streamlit as st
from ui_utils import check_password
from pdf_to_quizz import pdf_to_quizz
from text_to_quizz import txt_to_quizz
from generate_pdf import generate_pdf_quiz
import json
# for QR
import qrcode
from datetime import datetime
from PIL import Image
import streamlit as st
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask

generated_qrcodes_path = "generated_qrcodes/"
# to here
import asyncio

st.set_page_config(page_title = "Najmah", page_icon="⭐", layout = "wide")

st.title("☆☆ Najmah | نـجـمـة ☆☆")
st.sidebar.title("Najmah Platform ")

def build_question(count, json_question):

    if json_question.get(f"question") is not None:
        st.write("Question: ", json_question.get(f"question", ""))
        choices = ['A', 'B', 'C', 'D']
        selected_answer = st.selectbox(f"Select your answer:", choices, key=f"select_{count}")
        for choice in choices:
            choice_str = json_question.get(f"{choice}", "None")
            st.write(f"{choice} {choice_str}")
                    
        color = ""
        if st.button("Submit", key=f"button_{count}"):
            rep = json_question.get(f"reponse")
            if selected_answer == rep:
                color = ":green"
                st.write(f":green[correct answer: {rep}]")
                
            else:
                color = ":red"
                st.write(f":red[wrong answer. the correct answer is: {rep}].")                

        st.write(f"{color}[Your answer: {selected_answer}]")

        count += 1

    return count

def generate_qrcode(url):
    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=2
                        )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=StyledPilImage, color_mask=HorizontalGradiantColorMask())

    current_ts = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    qrcode_path = generated_qrcodes_path + "qrcode_" + str(current_ts) + ".png"
    img.save(qrcode_path)
    return qrcode_path

# Upload PDF file
uploaded_file = st.file_uploader("", type=["pdf"])
#txt = st.text_area('Taper le texte à partir duquel vous voulez générer le quizz')
#if st.button("Générer Quiz", key=f"button_generer"):
 #   if txt is not None:
  #      with st.spinner("Génération du quizz..."):
   #         st.session_state['questions'] = asyncio.run(txt_to_quizz(txt))
    #        st.write("Quizz généré avec succès!")

if st.button("Generate Quiz", key=f"button_generer"):
 if uploaded_file is not None:    
    old_file_name = st.session_state.get('uploaded_file_name', None)
    if (old_file_name != uploaded_file.name):
        # Convert PDF to text
        with st.spinner("Generation on process..."):

            with open(f"data/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getvalue())        

            # Initialize session state
            st.session_state['uploaded_file_name'] = uploaded_file.name
            st.session_state['questions'] = asyncio.run(pdf_to_quizz(f"data/{uploaded_file.name}"))

            st.write("Quiz generated successfully!🎉")
            # url = st.text_input("⚠ Enter the Quiz URL to share with your students! 👇")
            # if url is not None and url != "":
            #     with st.spinner(f"Generating QR Code... 💫"):
            #         qrcode_path = generate_qrcode(str(url))

            #     col1, col2, col3 = st.columns(3)
            #     with col1:
            #         st.write(' ')
            #     with col2:
            #         image = Image.open(qrcode_path)
            #         st.image(image, caption='Here\'s the Generated QR Code ✅')
            #     with col3:
            #         st.write(' ')
  # FOR QUESTION
#if ('questions' in st.session_state):
    # Display question
 #   count = 0
  #  for json_question in st.session_state['questions']:
#
 #       count = build_question(count, json_question)
        
    # generate pdf quiz
    #
    # if st.button("Generate PDF Quiz", key=f"button_generer_quiz"):
    #     with st.spinner("Generating the quiz in PDF..."):
    #         json_questions = st.session_state['questions']
    #         # save into a file
    #         file_name = uploaded_file.name

    #         # remove extension .pdf from file name
    #         if file_name.endswith(".pdf"):
    #             file_name = file_name[:-4]

    #         with open(f"data/quiz-{file_name}.json", "w", encoding='latin-1', errors='ignore') as f:
    #             str = json.dumps(json_questions)
    #             f.write(str)

    #         generate_pdf_quiz(f"data/quiz-{file_name}.json", json_questions)
            
    #         st.write("PDF Quiz generated successfully!")        





#main_image = Image.open('static/main_banner.png')

#st.image(main_image,use_column_width='auto')
#st.title("✨ QR Code Generator 🚀")


#else:
 #   st.warning('⚠ Please enter the Quiz URL to share with your students! 😯')

url = st.text_input("⚠ Enter the Quiz URL to share with your students! 👇")
if url is not None and url != "":
    with st.spinner(f"Generating QR Code... 💫"):
        qrcode_path = generate_qrcode(str(url))
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            image = Image.open(qrcode_path)
            st.image(image, caption='Here\'s the Generated QR Code ✅')
        with col3:
            st.write(' ')

