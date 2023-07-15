import streamlit as st

#To work with requests and APIs
import requests

#To operate with date and times
import datetime

#To open pickles with model and transformers info
import pickle

#For making plots
import matplotlib.pyplot as plt


#To load the key from .env and get access to stored variables
#from dotenv import load_dotenv
import os
import sys

from streamlit_functions.functions import fetch_match, unique_tier, find_image, offset_image, prediction, match_result_team, diagnosis, queues_dict, region_dict, columns_of_interest,macro_region,match_type_list, tier_list

sys.path.insert(0,os.path.abspath(".."))

#Get value stored in variable
api_key = st.secrets["API_KEY"]

st.set_page_config(
            page_title="Oldies", # Adjust things later
            page_icon=":hourglass_flowing_sand:", #Change icon later
            layout="wide", # or centered, wide has more space
            initial_sidebar_state="auto") # collapsed

#Page Title
st.title('Oldies :hourglass_flowing_sand:')

#Main Form to get data from user
with st.form(key='params_for_api'):

    columns = st.columns(4)

    match_id = columns[0].text_input("Game ID", help = "You can find the Game ID in League of Legends -> Profile -> Match History", value= "1316687991")

    chosen_region = columns[1].selectbox("Region", region_dict.keys(), help = "Region for this Game ID", index= 0) #Default Index correspond to KR

    league = columns[2].selectbox("Choose the Tier for this Match", tier_list, help = "The Tier defines de Trained Model used to Predict the result", index= 1) #Default Index correspond to Ranked

    team = columns[3].selectbox("Choose team to analyse", ["Blue","Red"], help = "The team to analyze", index= 0)

    st.form_submit_button('Make prediction')

#Converts user input to region ID
region = region_dict[chosen_region]


st.write(f" ")
st.write(f" ")

#Obtain Match Final Data
try:
    path_match_timeline =f"https://{macro_region[str(region)]}.api.riotgames.com/lol/match/v5/matches/{region_dict[chosen_region]}_{match_id}?api_key={api_key}"
    match_final = requests.get(path_match_timeline).json()
    #To find match type using queues_dict
    match_type_key = match_final["info"]["queueId"]
except:
    st.write("Could not find match, please verify Match ID and Region")
    st.stop()



if match_type_key in [450, 720]:
    st.write("Model not optimized for ARAM games")
    st.stop()

#Obtain Match Timeline Data
try:
    path_match_timeline =f"https://{macro_region[str(region)]}.api.riotgames.com/lol/match/v5/matches/{region_dict[chosen_region]}_{match_id}/timeline?api_key={api_key}"
    match_timeline = requests.get(path_match_timeline).json()
    match_length = len(match_timeline["info"]['frames'])
except:
    st.write("Could not find match, please verify Match ID and Region")
    st.stop()


if match_length < 10:
    st.write("Match to short, :notes:No retreat, baby, no surrender	:musical_note:")
    st.stop()

#Obtains unx timestamp and converts it into date time
formatted_date = datetime.datetime.fromtimestamp(match_final["info"]["gameStartTimestamp"]/1000).strftime('%Y-%m-%d %H:%M')

#Generates columns for displaying match data
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,1,0.18,1,1,1,0.18,1])


#Info for loading model
look_events=["CHAMPION_SPECIAL_KILL","CHAMPION_KILL","ELITE_MONSTER_KILL","BUILDING_KILL"]
pickle_file_path = f"model/pickles_models/{league}_model.pkl"
with open(pickle_file_path, "rb") as file:
    # Load the data from the pickle file
    fitted_model = pickle.load(file)


#For setting the columns to display results
with col1:
    st.markdown("##### Date")
    st.write(f"{formatted_date}")
    st.write("##### Studied Side:")
    if team == "Blue":
        st.write("##### :blue[Blue Team]")
    else:
        st.write("##### :red[Red Team]")
with col2:
    st.write("##### Match Type")
    st.write(f"{queues_dict[match_type_key]}")

with col3:
    st.write("##### :blue[Img]")
with col4:
    st.write("##### :blue[Champion]")
with col5:
    st.write("##### :blue[KDA]")
with col6:
    st.write("##### :red[KDA]")
with col7:
    st.write("##### :red[Img]")
with col8:
    st.write("##### :red[Champion]")

#Evaluates match lenght and create a list of minutes
minute = 10 #This is arbitrary were we are evaluating if it was a comeback or not
#match_length = len(match_timeline["info"]['frames'])
minute_list = list(range(match_length))

#Loops both teams at the same time
for participant in range(5):
    #position1 = match_final["info"]["participants"][participant]["teamPosition"]
    champion1 = match_final["info"]["participants"][participant]["championName"]
    kill1 = match_final["info"]["participants"][participant]["kills"]
    assist1 = match_final["info"]["participants"][participant]["assists"]
    death1 = match_final["info"]["participants"][participant]["deaths"]
    #position1 = match_final["info"]["participants"][participant+5]["teamPosition"]
    champion2 = match_final["info"]["participants"][participant+5]["championName"]
    kill2 = match_final["info"]["participants"][participant+5]["kills"]
    assist2 = match_final["info"]["participants"][participant+5]["assists"]
    death2 = match_final["info"]["participants"][participant+5]["deaths"]


    with col3:
        st.image(find_image(champion1), width=25)
    with col4:
        st.write(f":blue[{champion1}]")
    with col5:
        st.write(f":blue[{kill1}/{death1}/{assist1}]")
    with col6:
        st.write(f":red[{kill2}/{death2}/{assist2}]")
    with col7:
        st.image(find_image(champion2), width=25)
    with col8:
        st.write(f":red[{champion2}]")


#Defines user team and color for plots
if team == "Blue":
    proba_position = 1
    color = "royalblue"
    color1 = "blue"
if team == "Red": #if player is from team 2, its probability of winning is equal to team 1 probability of losing
    proba_position = 0
    color = "red"
    color1 = "red"

api_model_response = prediction(match_timeline,minute_list,look_events,columns_of_interest, fitted_model, proba_position, league)

proba = round(api_model_response[minute],2)

columns3 = st.columns(3)

gold_earned = [match_final["info"]["participants"][i]["goldEarned"] for i in range(10)]
champ_list = [match_final["info"]["participants"][i]["championName"] for i in range(10)]
colors = ['#008CBA'] * 5 + ['#E9422E'] * 5


fig, ax = plt.subplots()
#fig.set_facecolor('blue')
ax.bar(champ_list, gold_earned, color=colors)
ax.set_title('Total Gold Earned')
ax.get_xaxis().set_visible(False)
for i, c in enumerate(champ_list):
    offset_image(i, c, ax)
columns3[0].pyplot(fig)

fig1, ax1 = plt.subplots()
ax1.plot(minute_list, api_model_response, color=color, marker='o')
ax1.set_title('Winning Propability (%) vs Match Time (min)')
ax1.set_ylim([0, 100])
columns3[1].pyplot(fig1)

if proba >= 50:
    st.write(f"##### Probability of :{color1}[{team}] team winning at minute {minute} was {proba}% :chart_with_upwards_trend:")
else:
    st.write(f"##### Probability of :{color1}[{team}] team winning at minute {minute} was {proba}% :chart_with_downwards_trend:")

result = match_result_team(match_final, team)

if result == "Victory":
    st.write(f"##### :{color1}[{team}] team result: {result} :trophy:")
else:
    st.write(f"##### :{color1}[{team}] team result: {result} :thumbsdown:")

st.write(f"##### {diagnosis(proba, result)}")
