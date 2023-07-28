import streamlit as st

with open("riot.txt", "r") as file:
    btn = st.download_button(
            label="riot.txt",
            data=file,
            file_name="riot.txt",

          )
