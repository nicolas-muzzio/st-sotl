import streamlit as st
import streamlit.components.v1 as components  # Import Streamlit


st.set_page_config(
            page_title="Spirit of the LoL", # Adjust things later
            page_icon=":bar_chart:", #Change icon later
            layout="wide", # or centered, wide has more space
            initial_sidebar_state="auto") # collapsed

st.write("# Welcome to Spirit of the LoL! 👋")

st.sidebar.success("Select an app above")

st.write("#### Spirit of the LoL is a project that aims to apply Data Science and Machine Learning tools to League of Legends")

st.write("")

st.write("")

st.write("#### **👈 Select an app from the sidebar**")

st.write("")

st.write("")

st.write("##### **OddsMeter** :video_game:: know the winning odds of your last games and if you :orange[Led but Lost] :collision: or you :green[Defied the Odds] :heart_on_fire:")
st.write("##### :link: https://spirit-of-the-lol.streamlit.app/OddsMeter")

st.write("")

st.write("")

st.write("##### **Predictor** :dart:: select team objective differences to predict if your team will end in Victory :trophy: or Defeat :thumbsdown:")
st.write("##### :link: https://spirit-of-the-lol.streamlit.app/Predictor")

st.write("")

st.write("")

st.write("##### **Oldies** :hourglass_flowing_sand:: know the winning odds of old games :open_file_folder:")
st.write("##### :link: https://spirit-of-the-lol.streamlit.app/Oldies")

st.write("")

st.write("")

st.write("##### **The Team** :busts_in_silhouette::busts_in_silhouette:: to know more about us")
st.write("##### :link: https://spirit-of-the-lol.streamlit.app/The_Team")

st.write("")

st.write("")

st.write("")

st.write("")

with open("riot.txt", "r") as file:
    btn = st.download_button(
            label="Download riot.txt",
            data=file,
            file_name="riot.txt",


          )


components.html("<a href=file://wsl.localhost/Ubuntu/home/nicolasemuzzio/code/nicolas-muzzio/st-sotl/riot.txt download=riot.txt>riot.txt</a>")

st.write("")

st.write("")

st.write("")

st.write("")

st.write("Spirit of the LoL is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc")
