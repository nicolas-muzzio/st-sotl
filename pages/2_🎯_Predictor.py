import streamlit as st

#To open pickles with model and transformers info
import pickle

import pandas as pd

from preprocessing.clean_preprocess import preprocess_pred

def find_transformer(minute):
    """
    Calculate the closest transformer, load the transformer from the pickle file and returns it
    """
    if minute > 24:
        transformer_file_path = f"preprocessing/pickles_transformers/30/{league}_transformer.pkl"
        with open(transformer_file_path, "rb") as transformer_file:
        # Load the transformer from the pickle file
            transformer = pickle.load(transformer_file)
        return transformer
    else:
        minute_t = (24//5 + 1) * 5
        transformer_file_path = f"preprocessing/pickles_transformers/{minute_t}/{league}_transformer.pkl"
        with open(transformer_file_path, "rb") as transformer_file:
            transformer = pickle.load(transformer_file)
        return transformer


columns_of_interest_dict = {5: {'killType_KILL_ACE': 0,
        'killType_KILL_FIRST_BLOOD': 1,
        'killType_KILL_MULTI': 3,
        'minionsKilled': 40,
        'monsterType_AIR_DRAGON': 0,
        'monsterType_CHEMTECH_DRAGON' :0,
        'monsterType_EARTH_DRAGON' :0,
        'monsterType_FIRE_DRAGON' :0,
        'monsterType_HEXTECH_DRAGON' :0,
        'monsterType_RIFTHERALD' :0,
        'monsterType_WATER_DRAGON' :0,
        'monsterType_ELDER_DRAGON' :0,
        'monsterType_BARON_NASHOR' :0,
        'totalGold' : 4000,
        'towerType_INNER_TURRET' : 0,
        'towerType_OUTER_TURRET' : 0,
        'towerType_BASE_TURRET' : 0,
        'buildingType_INHIBITOR_BUILDING' : 0},

                            10: {'killType_KILL_ACE': 2,
        'killType_KILL_FIRST_BLOOD': 1,
        'killType_KILL_MULTI': 5,
        'minionsKilled': 80,
        'monsterType_AIR_DRAGON': 1,
        'monsterType_CHEMTECH_DRAGON' :1,
        'monsterType_EARTH_DRAGON' :1,
        'monsterType_FIRE_DRAGON' :1,
        'monsterType_HEXTECH_DRAGON' :1,
        'monsterType_RIFTHERALD' :1,
        'monsterType_WATER_DRAGON' :1,
        'monsterType_ELDER_DRAGON' :0,
        'monsterType_BARON_NASHOR' :0,
        'totalGold' : 12000,
        'towerType_INNER_TURRET' : 3,
        'towerType_OUTER_TURRET' : 3,
        'towerType_BASE_TURRET' : 0,
        'buildingType_INHIBITOR_BUILDING' : 0},

                            15: {'killType_KILL_ACE': 3,
        'killType_KILL_FIRST_BLOOD': 1,
        'killType_KILL_MULTI': 8,
        'minionsKilled': 120,
        'monsterType_AIR_DRAGON': 1,
        'monsterType_CHEMTECH_DRAGON' :1,
        'monsterType_EARTH_DRAGON' :1,
        'monsterType_FIRE_DRAGON' :1,
        'monsterType_HEXTECH_DRAGON' :1,
        'monsterType_RIFTHERALD' :2,
        'monsterType_WATER_DRAGON' :1,
        'monsterType_ELDER_DRAGON' :0,
        'monsterType_BARON_NASHOR' :0,
        'totalGold' : 20000,
        'towerType_INNER_TURRET' : 3,
        'towerType_OUTER_TURRET' : 3,
        'towerType_BASE_TURRET' : 3,
        'buildingType_INHIBITOR_BUILDING' : 3},

                            20: {'killType_KILL_ACE': 4,
        'killType_KILL_FIRST_BLOOD': 1,
        'killType_KILL_MULTI': 15,
        'minionsKilled': 160,
        'monsterType_AIR_DRAGON': 1,
        'monsterType_CHEMTECH_DRAGON' :1,
        'monsterType_EARTH_DRAGON' :1,
        'monsterType_FIRE_DRAGON' :1,
        'monsterType_HEXTECH_DRAGON' :1,
        'monsterType_RIFTHERALD' :2,
        'monsterType_WATER_DRAGON' :1,
        'monsterType_ELDER_DRAGON' :0,
        'monsterType_BARON_NASHOR' :0,
        'totalGold' : 25000,
        'towerType_INNER_TURRET' : 3,
        'towerType_OUTER_TURRET' : 3,
        'towerType_BASE_TURRET' : 3,
        'buildingType_INHIBITOR_BUILDING' : 6},

                            25: {'killType_KILL_ACE': 5,
        'killType_KILL_FIRST_BLOOD': 1,
        'killType_KILL_MULTI': 20,
        'minionsKilled': 200,
        'monsterType_AIR_DRAGON': 2,
        'monsterType_CHEMTECH_DRAGON' :2,
        'monsterType_EARTH_DRAGON' :2,
        'monsterType_FIRE_DRAGON' :2,
        'monsterType_HEXTECH_DRAGON' :2,
        'monsterType_RIFTHERALD' :2,
        'monsterType_WATER_DRAGON' :2,
        'monsterType_ELDER_DRAGON' :1,
        'monsterType_BARON_NASHOR' :1,
        'totalGold' : 30000,
        'towerType_INNER_TURRET' : 3,
        'towerType_OUTER_TURRET' : 3,
        'towerType_BASE_TURRET' : 3,
        'buildingType_INHIBITOR_BUILDING' : 9},

                            30: {'killType_KILL_ACE': 6,
        'killType_KILL_FIRST_BLOOD': 1,
        'killType_KILL_MULTI': 25,
        'minionsKilled': 240,
        'monsterType_AIR_DRAGON': 3,
        'monsterType_CHEMTECH_DRAGON' :3,
        'monsterType_EARTH_DRAGON' :3,
        'monsterType_FIRE_DRAGON' :3,
        'monsterType_HEXTECH_DRAGON' :3,
        'monsterType_RIFTHERALD' :2,
        'monsterType_WATER_DRAGON' :3,
        'monsterType_ELDER_DRAGON' :2,
        'monsterType_BARON_NASHOR' :2,
        'totalGold' : 35000,
        'towerType_INNER_TURRET' : 3,
        'towerType_OUTER_TURRET' : 3,
        'towerType_BASE_TURRET' : 3,
        'buildingType_INHIBITOR_BUILDING' : 12}
                            }


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

league = columns[1].selectbox("Tier",tier_list ,index=2, label_visibility = "collapsed")


if time == None:
    st.stop()

#Main Form to get data from user
with st.form(key='params_for_api'):

    st.write("Explanation: a positive difference means the team has taken more of that particular objective than the other team.")
    st.write("""Disclaimer:
             -This model does not account for side difference.
             -Some combinations of inputs may not be possible in the game (e.g.: having more than 3 elemental dragons)""")

    columns2 = st.columns(3)

    columns2[0].write("#### Total Gold Differences")
    totalGold = columns2[0].slider("Total Gold Difference",
                                    min_value=-columns_of_interest_dict[time]["totalGold"],
                                    max_value=columns_of_interest_dict[time]["totalGold"],
                                    value=0, step=None,
                                    format=None, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False,
                                    label_visibility="collapsed")

    columns2[1].write("#### Minions Killed Difference")
    minionsKilled = columns2[1].slider("Minions Killed Difference",
                                        min_value=-columns_of_interest_dict[time]["minionsKilled"],
                                        max_value=columns_of_interest_dict[time]["minionsKilled"],
                                        value=0, step=None,
                                        format=None, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False,
                                        label_visibility="collapsed")

    st.write("")

    st.write("#### Building Objectives Differences")
    columns5 = st.columns(4)

    outer_turret_list = list(range(-columns_of_interest_dict[time]["towerType_OUTER_TURRET"],columns_of_interest_dict[time]["towerType_OUTER_TURRET"]+1))
    towerType_OUTER_TURRET = columns5[0].selectbox("Outer Turret", outer_turret_list,index=columns_of_interest_dict[time]["towerType_OUTER_TURRET"])

    inner_turret_list = list(range(-columns_of_interest_dict[time]["towerType_INNER_TURRET"],columns_of_interest_dict[time]["towerType_INNER_TURRET"]+1))
    towerType_INNER_TURRET = columns5[1].selectbox("Innter Turret",inner_turret_list ,index=columns_of_interest_dict[time]["towerType_INNER_TURRET"])
    #inhibitort = columns5[2].selectbox("inhibitort",tier_list ,index=0)

    base_turret_list = list(range(-columns_of_interest_dict[time]["towerType_BASE_TURRET"],columns_of_interest_dict[time]["towerType_BASE_TURRET"]+1))
    towerType_BASE_TURRET = columns5[2].selectbox("Inhibitor Turret",base_turret_list ,index=columns_of_interest_dict[time]["towerType_BASE_TURRET"])

    inhibitor_list = list(range(-columns_of_interest_dict[time]["buildingType_INHIBITOR_BUILDING"],columns_of_interest_dict[time]["buildingType_INHIBITOR_BUILDING"]+1))
    buildingType_INHIBITOR_BUILDING = columns5[3].selectbox("Inhibitor",inhibitor_list ,index=columns_of_interest_dict[time]["buildingType_INHIBITOR_BUILDING"])

    st.write("")

    st.write("#### Jungle Objectives Differences")
    st.write("##### Dragons")
    columns3 = st.columns(7)

    dragon_list = list(range(-columns_of_interest_dict[time]["monsterType_AIR_DRAGON"],columns_of_interest_dict[time]["monsterType_AIR_DRAGON"]+1))


    monsterType_FIRE_DRAGON = columns3[0].selectbox("Fire",dragon_list ,index=columns_of_interest_dict[time]["monsterType_AIR_DRAGON"])
    monsterType_WATER_DRAGON = columns3[1].selectbox("Water",dragon_list ,index=columns_of_interest_dict[time]["monsterType_AIR_DRAGON"])
    monsterType_EARTH_DRAGON = columns3[2].selectbox("Earth",dragon_list ,index=columns_of_interest_dict[time]["monsterType_AIR_DRAGON"])
    monsterType_CHEMTECH_DRAGON = columns3[3].selectbox("Chemtech",dragon_list ,index=columns_of_interest_dict[time]["monsterType_AIR_DRAGON"])
    monsterType_HEXTECH_DRAGON = columns3[4].selectbox("Hextech",dragon_list ,index=columns_of_interest_dict[time]["monsterType_AIR_DRAGON"])
    monsterType_AIR_DRAGON = columns3[5].selectbox("Air",dragon_list ,index=columns_of_interest_dict[time]["monsterType_AIR_DRAGON"])

    elder_dragon_list = list(range(-columns_of_interest_dict[time]["monsterType_ELDER_DRAGON"],columns_of_interest_dict[time]["monsterType_ELDER_DRAGON"]+1))
    monsterType_ELDER_DRAGON = columns3[6].selectbox("Elder",elder_dragon_list ,index=columns_of_interest_dict[time]["monsterType_ELDER_DRAGON"])

    st.write("")

    columns4 = st.columns(6)

    herald_list = list(range(-columns_of_interest_dict[time]["monsterType_RIFTHERALD"],columns_of_interest_dict[time]["monsterType_RIFTHERALD"]+1))
    columns4[0].write("##### Hearld")
    monsterType_RIFTHERALD = columns4[0].selectbox("Rift Herald",herald_list ,index=columns_of_interest_dict[time]["monsterType_RIFTHERALD"],label_visibility="collapsed")

    nashor_list = list(range(-columns_of_interest_dict[time]["monsterType_BARON_NASHOR"],columns_of_interest_dict[time]["monsterType_BARON_NASHOR"]+1))
    columns4[1].write("##### Baron")
    monsterType_BARON_NASHOR = columns4[1].selectbox("Baron Nashor",nashor_list ,index=columns_of_interest_dict[time]["monsterType_BARON_NASHOR"],label_visibility="collapsed")

    #st.write("#### Champion Kills Differences")

    #columns6 = st.columns(3)
    #columns6[0].write("##### First Blood")
    killType_KILL_FIRST_BLOOD = 0 #columns6[0].selectbox("First Blood",[-1,0,1] ,index=1,label_visibility="collapsed")

    #multi_kill_list = list(range(-columns_of_interest_dict[time]["killType_KILL_MULTI"],columns_of_interest_dict[time]["killType_KILL_MULTI"]+1))
    #columns6[1].write("##### Multi Kills")
    killType_KILL_MULTI = 0 #columns6[1].selectbox("Multi Kills",multi_kill_list ,index=columns_of_interest_dict[time]["killType_KILL_MULTI"],label_visibility="collapsed")

    #multi_kill_list = list(range(-columns_of_interest_dict[time]["killType_KILL_ACE"],columns_of_interest_dict[time]["killType_KILL_ACE"]+1))
    #columns6[1].write("##### Aces")
    killType_KILL_ACE = 0 #columns6[1].selectbox("Aces",multi_kill_list ,index=columns_of_interest_dict[time]["killType_KILL_ACE"],label_visibility="collapsed")

    st.form_submit_button('Make prediction')

data_dict = {'killType_KILL_ACE': killType_KILL_ACE,
        'killType_KILL_FIRST_BLOOD': killType_KILL_FIRST_BLOOD,
        'killType_KILL_MULTI': killType_KILL_MULTI,
        'minionsKilled': minionsKilled,
        'monsterType_AIR_DRAGON': monsterType_AIR_DRAGON,
        'monsterType_CHEMTECH_DRAGON' :monsterType_CHEMTECH_DRAGON,
        'monsterType_EARTH_DRAGON' :monsterType_EARTH_DRAGON,
        'monsterType_FIRE_DRAGON' :monsterType_FIRE_DRAGON,
        'monsterType_HEXTECH_DRAGON' :monsterType_HEXTECH_DRAGON,
        'monsterType_RIFTHERALD' :monsterType_RIFTHERALD,
        'monsterType_WATER_DRAGON' :monsterType_WATER_DRAGON,
        'monsterType_ELDER_DRAGON' :monsterType_ELDER_DRAGON,
        'monsterType_BARON_NASHOR' :monsterType_BARON_NASHOR,
        'totalGold' : totalGold,
        'towerType_INNER_TURRET' : towerType_INNER_TURRET,
        'towerType_OUTER_TURRET' : towerType_OUTER_TURRET,
        'towerType_BASE_TURRET' : towerType_BASE_TURRET,
        'buildingType_INHIBITOR_BUILDING' : buildingType_INHIBITOR_BUILDING}

data_df = pd.DataFrame(data_dict, index=[0])

pickle_file_path = f"model/pickles_models/{league}_model.pkl"
with open(pickle_file_path, "rb") as file:
        # Load the data from the pickle file
        fitted_model = pickle.load(file)

transformer = find_transformer(time)

#st.write(data_df)

X_pred_prep = preprocess_pred(data_df, transformer)

model = fitted_model

proba = round(model.predict_proba(X_pred_prep)[0][1]*100,2)

#To compensate for side difference that we are not taking ino account
if (data_df == 0).all(axis=1).all():
    proba = 50.0

st.write(f"### The propability of winning is {proba}")
