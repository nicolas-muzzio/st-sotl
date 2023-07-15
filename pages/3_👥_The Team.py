import streamlit as st


st.set_page_config(
            page_title="Spirit of the LoL", # Adjust things later
            page_icon="👥", #Change icon later
            layout="wide", # or centered, wide has more space
            initial_sidebar_state="auto") # collapsed

st.write("# The Team :mechanical_arm:")

st.write("#### We are Le Wagoners! Data Science Bootcamp Batch 1201")

st.write("#### ")

columns = st.columns(5)

columns[0].write("#### Name")
columns[1].write("#### Andy")
columns[2].write("#### Gonza")
columns[3].write("#### Santy")
columns[4].write("#### Nico")

columns[0].write("")
columns[0].write("")


columns[0].write("#### A Champion")
columns[1].image(f"images/champion/4155.png",caption="4155", width=100)
columns[2].image(f"images/champion/4155.png",caption="4155", width=100)
columns[3].image(f"images/champion/4155.png",caption="4155", width=100)
columns[4].image(f"images/champion/Ahri.png",caption="Ahri", width=100)

columns[0].write("")
columns[0].write("")
columns[0].write("")
columns[0].write("")

columns[0].write("#### An Emote")
columns[1].write("#### Andy")
columns[2].write("#### Gonza")
columns[3].write("#### Santy")
columns[4].write("#### :microscope:")

columns[0].write("#### A Video Game")
columns[1].write("#### Andy")
columns[2].write("#### Gonza")
columns[3].write("#### Santy")
columns[4].write("#### Warcraft II")

st.write("#### ")

st.write("#### :email:Contact: lwdatasciencefinalproject@gmail.com")
