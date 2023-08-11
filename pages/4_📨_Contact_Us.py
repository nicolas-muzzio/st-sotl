import streamlit as st
from streamlit_functions.functions import check_text,check_email,check_inputs_contact,send_email


def check_form(user_name,user_email,subject,message_text):

    if check_inputs_contact(user_name,user_email,subject,message_text):
        send_email(user_name,user_email,subject,message_text)

        # Disable the submit button after it is clicked
        st.session_state.disabled = True

        st.write("##### :green[Your message has been sent :incoming_envelope:, thank you!!!]")
        st.write("##### To send another message, please, reload the page.")

    else:
        st.write("##### :orange[Please, check all required fields are filled :ballot_box_with_check]")


st.set_page_config(
            page_title="Contact Us", # Adjust things later
            page_icon="📨", #Change icon later
            layout="wide", # or centered, wide has more space
            initial_sidebar_state="auto") # collapsed

# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

st.title('Contact Us :incoming_envelope:')

st.write("#### Complete the required fields and press the Submit button")

columns = st.columns(2)

user_name = columns[0].text_input("Your name:", max_chars = 75)
if not check_text(user_name,1):
    columns[0].write(":red[Please, introduce a valid name]")

user_email = columns[1].text_input("Your email:", max_chars = 75)
if not check_email(user_email):
        columns[1].write(":red[Please, introduce a valid email]")

subject = st.text_input("Subject:", max_chars  = 150)
if not check_text(subject,3):
        st.write(":red[Please, describe the subject of your message]")

message_text = st.text_area("Message:", height = 275, max_chars = 3000)
if not check_text(message_text,6):
        st.write(":red[Please, write your message]")

columns2 = st.columns(11)

with columns2[0].form(key='contact_data', clear_on_submit=False):

    st.form_submit_button('Submit', disabled = st.session_state.disabled,
                          on_click= check_form, args = (user_name, user_email,subject,message_text))

st.write("")

st.write("")

st.write("")

st.write("")

st.write("Spirit of the LoL is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc")
