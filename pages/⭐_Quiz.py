import streamlit as st
st.sidebar.title("Najmah Platform ")
st.title("☆☆ Quiz ☆☆")
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
                st.write(f":green[You Got 3 Pts🏅]")
                #st.write("")
                st.balloons()
                
            else:
                color = ":red"
                st.write(f":red[Try again😔]")               

        #st.write(f"{color}[Your answer: {selected_answer}]")

        count += 1

    return count
if ('questions' in st.session_state):
    # Display question
    count = 0
    for json_question in st.session_state['questions']:

       count = build_question(count, json_question)