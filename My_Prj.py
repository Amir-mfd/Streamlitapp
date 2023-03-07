import streamlit as st
import pandas as pd

Movies = pd.read_csv('IMDB-Movie-Data.csv')
st.title("What to watch?")
st.subheader('Find your desired movie among 1000 titles:')
'--------'
Radio_Result = st.radio("How to search Movie?",("Title","Other Fields"))
if Radio_Result == "Title":
    # st.write("Title")
    User_Title = st.text_input('Movie name')
    Conditions = Movies['Title'].str.lower().str.contains(User_Title)
else:
    # st.write("Other")
    [user_year_1,user_year_2]=st.slider('Year',min_value=2005,max_value=2016,value=(2007,2014))
    Year_Condition = (Movies["Year"]>=user_year_1) & (Movies["Year"]<=user_year_2)
    user_Rate = st.number_input('Rate',min_value=2.0,max_value=10.0,step=0.5)
    Rate_Condition = Movies["Rating"]>=user_Rate
    Conditions = Year_Condition & Rate_Condition
    
    def repp(string):
        return string.split(',')
    genre_series = Movies['Genre'].apply(repp)
    set_genres = set()
    for genre_List in genre_series:
        for g in genre_List:
            set_genres.add(g.strip())
    
    user_genre = st.selectbox('Select Genre',sorted(set_genres))
    if user_genre:
        genre_Condition = Movies['Genre'].str.contains(user_genre)
        Conditions = Conditions & genre_Condition
    
    
    def repp2(actors):
        return actors.split(',')
    actor_series = Movies['Actors'].apply(repp2)
    set_actors = set()
    for actors in actor_series:
        for a in actors:
            set_actors.add(a.strip())
    user_actors = st.multiselect('Select actors',sorted(set_actors))   
    if len(user_actors)>0:
        actors_Condition = Movies['Actors'].str.contains(user_actors[0])
        for user_act in user_actors:
            actors_Condition = actors_Condition & Movies['Actors'].str.contains(user_actors)
        Conditions = Conditions & actors_Condition



# st.write(sorted(set_genres))
df = Movies[Conditions]
st.write('Number of Movies Found : ',len(df))
df
