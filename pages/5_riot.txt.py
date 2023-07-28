import streamlit as st
import streamlit.components.v1 as components  # Import Streamlit

with open("riot.txt", "r") as file:
    btn = st.download_button(
            label="riot.txt",
            data=file,
            file_name="riot.txt",

          )

#components.html("<a href=riot.txt download=riot.txt>riot.txt</a>")
