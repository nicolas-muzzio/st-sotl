import streamlit as st


st.set_page_config(
            page_title="Spirit of the LoL", # Adjust things later
            page_icon="🎯", #Change icon later
            layout="wide", # or centered, wide has more space
            initial_sidebar_state="auto") # collapsed

st.write("# Predictor 🎯")

tier_list = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]

time_list = [None, 5,10,15,20,25,30]

columns = st.columns(3)

columns[0].write("#### Match Time in minutes")
time = columns[0].selectbox("Match Time in minutes",time_list ,index=0, label_visibility = "collapsed")

columns[1].write("#### Tier")

tier = columns[1].selectbox("Tier",tier_list ,index=2, label_visibility = "collapsed")


if time == None:
    st.stop()

##################################################################
#Setear los min and max value segun los min and max values of each time, llamar los transformers en funcion del tiempo y el modelo en funcion del tier

#Main Form to get data from user
with st.form(key='params_for_api'):

    st.write("Explanation: a positive difference means the team has taken more of that particular objective than the other team.")

    columns2 = st.columns(3)

    columns2[0].write("#### Team Gold Difference")
    gold_diff = columns2[0].slider("Team Gold Difference", min_value=-1000, max_value=1000, value=0, step=None,
                          format=None, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="collapsed")

    columns2[1].write("#### Team Exp Difference")
    gold_diff = columns2[1].slider("Team Exp Difference", min_value=-1000, max_value=1000, value=0, step=None,
                          format=None, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="collapsed")

    st.write("")

    st.write("#### Building Objectives Difference")
    columns5 = st.columns(6)
    outert = columns5[0].selectbox("outert",tier_list ,index=0)
    innert = columns5[1].selectbox("innert",tier_list ,index=0)
    inhibitort = columns5[2].selectbox("inhibitort",tier_list ,index=0)
    baset = columns5[3].selectbox("baset",tier_list ,index=0)
    inhibitor = columns5[4].selectbox("inhibitor",tier_list ,index=0)

    st.write("")

    st.write("#### Jungle Objectives Difference")
    st.write("##### Dragons")
    columns3 = st.columns(6)
    infernal = columns3[0].selectbox("infernal",tier_list ,index=0)
    ocean = columns3[1].selectbox("ocean",tier_list ,index=0)
    mountain = columns3[2].selectbox("mountain",tier_list ,index=0)
    chem = columns3[3].selectbox("chem",tier_list ,index=0)
    hex = columns3[4].selectbox("hex",tier_list ,index=0)
    elder = columns3[5].selectbox("elder",tier_list ,index=0)

    st.write("")

    columns4 = st.columns(6)
    columns4[0].write("##### Hearld")
    herald = columns4[0].selectbox("herald",tier_list ,index=0,label_visibility="collapsed")
    columns4[1].write("##### Baron")
    baron = columns4[1].selectbox("baron",tier_list ,index=0,label_visibility="collapsed")

    st.form_submit_button('Make prediction')
