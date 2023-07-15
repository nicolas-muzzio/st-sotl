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

from streamlit_functions.functions import fetch_match, unique_tier, find_image, offset_image, prediction, match_result, diagnosis, queues_dict, region_dict, columns_of_interest,macro_region,match_type_list

sys.path.insert(0,os.path.abspath(".."))

#Get value stored in variable
api_key = st.secrets["API_KEY"]

st.set_page_config(
            page_title="Oldies", # Adjust things later
            page_icon=":hourglass_flowing_sand:", #Change icon later
            layout="wide", # or centered, wide has more space
            initial_sidebar_state="auto") # collapsed

#Page Title
st.title('NoobMeter :video_game:')

#Main Form to get data from user
with st.form(key='params_for_api'):

    columns = st.columns(3)

    summoner_name = columns[0].text_input("What is your Summoner Name?", value="hideonbush") #Default SummonerName corresponds to T1 Faker

    chosen_region = columns[1].selectbox("Choose your Region", help ="The region of your account", options = region_dict.keys(), index= 10) #Default Index correspond to KR

    chosen_match_type = columns[2].selectbox("Choose the Match Type", options = match_type_list.keys(), help = "The type of games you want to see", index= 1) #Default Index correspond to Ranked

    st.form_submit_button('Make prediction')

#Converts user input to region ID
region = region_dict[chosen_region]

#Converts user input to region ID
match_type = match_type_list[chosen_match_type]

#puuid and encrypted_summonerID obtention

path_puuid = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}'
try:
    summoner_data = requests.get(path_puuid).json()
    puuid = summoner_data['puuid']
except:
    st.write("Summoner not found, please check Summoner Name and Region")
    st.stop()

encrypted_summonerID = summoner_data['id']

#Tiers obtention -> needed to know which model we need to use
path_tier = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_summonerID}?api_key={api_key}"
ranked_tiers = requests.get(path_tier).json()

#Obtain the tier info if the summoner has any
no_tier = False
solo_tier = 0
flex_tier = 0
if ranked_tiers == []:
    no_tier = True
else:
    for i in range(len(ranked_tiers)):
        if ranked_tiers[i]["queueType"] == "RANKED_SOLO_5x5":
            solo_tier = ranked_tiers[i]["tier"]
        else:
            flex_tier = ranked_tiers[i]["tier"]

#match id obtention
matches = fetch_match(puuid, api_key, region, match_type, count = 20)

#Display Ranks
if no_tier:
    st.markdown("##### You do not have a ranked tier, probabilities of winning will be predicted considering a SILVER tier")
else:
    columns2 = st.columns(4)
    if solo_tier != 0:
        columns2[0].markdown(f"##### Your Solo Queue Tier is {solo_tier}")
    if flex_tier != 0:
        columns2[2].markdown(f"##### Your Flex Queue Tier is {flex_tier}")

st.write(f" ")
st.write(f" ")

if matches == []:
    st.write("No matches found, please check introduced data")
    st.stop()

match_counter = 0

for match in matches:

    #Obtain Match Final Data
    path_match_timeline =f"https://{macro_region[str(region)]}.api.riotgames.com/lol/match/v5/matches/{match}?api_key={api_key}"
    match_final = requests.get(path_match_timeline).json()


    #To find match type using queues_dict
    match_type_key = match_final["info"]["queueId"]

    if match_type_key in [450, 720]:
        continue

    #Obtain Match Timeline Data
    path_match_timeline =f"https://{macro_region[str(region)]}.api.riotgames.com/lol/match/v5/matches/{match}/timeline?api_key={api_key}"

    match_timeline = requests.get(path_match_timeline).json()

    match_length = len(match_timeline["info"]['frames'])

    if match_length < 10:
        continue

    #Obtains unx timestamp and converts it into date time
    formatted_date = datetime.datetime.fromtimestamp(match_final["info"]["gameStartTimestamp"]/1000).strftime('%Y-%m-%d %H:%M')

    #Generates columns for displaying match data
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,1,0.18,1,1,1,0.18,1])

    #Determines the user number of participant (if 0-4 is team 1, if 5-9 is team 2)
    user_participant = match_final["metadata"]["participants"].index(puuid)

    #Determines the user champion
    user_champion = match_final["info"]["participants"][user_participant]["championName"]


    #Info for loading model
    look_events=["CHAMPION_SPECIAL_KILL","CHAMPION_KILL","ELITE_MONSTER_KILL","BUILDING_KILL"]
    league=unique_tier(solo_tier,flex_tier)
    pickle_file_path = f"model/pickles_models/{league}_model.pkl"
    with open(pickle_file_path, "rb") as file:
        # Load the data from the pickle file
        fitted_model = pickle.load(file)


    #For setting the columns to display results
    with col1:
        st.markdown("##### Date")
        st.write(f"{formatted_date}")
        st.write("##### Player Side:")
        if user_participant < 5:
            st.write("##### :blue[Blue Team]")
        else:
            st.write("##### :red[Red Team]")
    with col2:
        st.write("##### Match Type")
        st.write(f"{queues_dict[match_type_key]}")
        st.write("##### Played Champion:")
        st.image(find_image(user_champion), caption = user_champion, width=90)
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
            if champion1 == user_champion:
                st.write(f"**:blue[{champion1}]** :arrow_left:")
            else:
                st.write(f":blue[{champion1}]")
        with col5:
            st.write(f":blue[{kill1}/{death1}/{assist1}]")
        with col6:
            st.write(f":red[{kill2}/{death2}/{assist2}]")
        with col7:
            st.image(find_image(champion2), width=25)
        with col8:
            if champion2 == user_champion:
                st.write(f"**:red[{champion2}]** :arrow_left:")
            else:
                st.write(f":red[{champion2}]")


    #Defines user team and color for plots
    if user_participant < 5:
        proba_position = 1
        color = "royalblue"
    if user_participant > 4: #if player is from team 2, its probability of winning is equal to team 1 probability of losing
        proba_position = 0
        color = "red"

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
        st.write(f"##### Probability of your team winning at minute {minute} was {proba}% :chart_with_upwards_trend:")
    else:
        st.write(f"##### Probability of your team winning at minute {minute} was {proba}% :chart_with_downwards_trend:")

    result = match_result(match_final, user_participant)

    if result == "Victory":
        st.write(f"##### Your team result: {result} :trophy:")
    else:
        st.write(f"##### Your team result: {result} :thumbsdown:")

    st.write(f"##### {diagnosis(proba, result)}")

    st.write(f" ")
    st.write(f" ")

    match_counter = match_counter + 1

    if match_counter == 1:
        break
