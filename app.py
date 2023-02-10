import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy


df = pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://www.freepnglogos.com/uploads/olympic-rings-png/olympic-rings-denver-fact-colorado-hates-the-olympic-games-the-4.png')
user_menu = st.sidebar.radio(
    'select an option',
    ('Medal Tally','Overall Analysis','Country Wise Analysis','Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)


    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'Medal Tally in {selected_year}')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f'Medal Tally of {selected_country}')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f'Medal Tally of {selected_country} in {selected_year}')
    st.table(medal_tally)


if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    st.title('Participating Nations Over Years')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    st.title('Events Over the Years')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    st.title('Athletes Over the Years')
    fig = px.line(athletes_over_time, x="Edition", y='Name')
    st.plotly_chart(fig)

    st.title('No of Events over time(Every Sport)')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country Wise Analysis':

    st.sidebar.title('Country Wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + "Medal Tally Over the Years")
    st.plotly_chart(fig)

    st.title(selected_country + "excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10Athletes of" + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


if user_menu == 'Athlete wise Analysis':
    athylet_df=df.drop_duplicates(['Name','region'])


    x1 = athylet_df['Age'].dropna()
    x2 = athylet_df[athylet_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athylet_df[athylet_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athylet_df[athylet_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                            show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=900,height=680)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)

    st.pyplot(fig)


    st.title("Men Vs Women Partcipation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=900, height=680)
    st.plotly_chart(fig)
