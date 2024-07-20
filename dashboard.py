import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st 
import json

st.set_page_config(
    layout='wide', 
    initial_sidebar_state='expanded'
)

data = pd.read_csv('data.csv')
view = pd.read_csv('view.csv')
view['Mean Episode Rating Count'] = round(view['Mean Episode Rating Count'])


lst = view['Genres'].tolist()
genres = []
for i in lst:
    genres += i.split(' ,')
genres = set(genres)



global_retings = list(set(view['Global Rating'].tolist()))

year = list(set(view['Start Year']))

def extract_genre_names(json_str):
        json_list = json.loads(json_str.replace("'", '"'))
    
        genre_names = [item['genre']['text'] for item in json_list]
    
        genre_names_str = ' ,'.join(genre_names)
        return genre_names_str

 # --------------------------------------------------------------- Data clear --------------------------------------------------------------------

def page_1():
    st.title("Bizga berilgan datalarni tozalash")

    df = pd.read_csv('imdb_top_250_series_episode_ratings.csv')
    df1 = pd.read_csv('imdb_top_250_series_global_ratings.csv')

    


    st.write("""
            ## Eng so'nggi IMDb(Internet film bazasi)dagi Top 250ta seriyallarni epizodlar reytinglari
""")
    st.dataframe(df)
    
    


    st.write("""
            ### Bizga berilgan datasetlarning asosiy ustunlarini olib qolib qolgani tashlab yuboramiz.
            Masalan bizga kerakli ustunlar seriallarni nomi, mavsumlar soni, epizodlar soni, reytinglari, sanalari va hokozolari.
            Tashlab yubormoqchi bolgan ustunlarimiz rasmni urllari, rasm balanligi, rasm eni, epizodlarni qisqa mazmuni shunga o'xshagan ustunlarni tashlab yuboramiz.
            
             
""")
    with st.expander('Kerakli ustunlarni olish'):
        code = """
    df = df[['title', 'season', 'episode', 'aggregateRating', 'voteCount', 'releaseDate.day', 
    'releaseDate.month', 'releaseDate.year', 'series.id']]

    df1 = df1[['currentRank', 'node.titleText.text', 'node.titleType.text', 'node.episodes.episodes.total',
    'node.releaseYear.year', 'node.releaseYear.endYear', 'node.ratingsSummary.aggregateRating', 
    'node.ratingsSummary.voteCount', 'node.runtime.seconds', 'node.titleGenres.genres', 'node.id']]
"""
        st.code(code, language='payhon')
        
    df = df[['title', 'season', 'episode', 'aggregateRating', 'voteCount', 'releaseDate.day', 'releaseDate.month', 'releaseDate.year', 'series.id']]
    df1 = df1[['currentRank', 'node.titleText.text', 'node.titleType.text', 'node.episodes.episodes.total', 'node.releaseYear.year', 'node.releaseYear.endYear', 'node.ratingsSummary.aggregateRating', 'node.ratingsSummary.voteCount', 'node.runtime.seconds', 'node.titleGenres.genres', 'node.id']]
    
    
    df1['node.runtime.seconds'] = df1['node.runtime.seconds'] / 60

    # ----------- janr ustunini parchalab tashladim --------------------

    df1['node.titleGenres.genres'] = df1['node.titleGenres.genres'].apply(extract_genre_names)

    # ---------------------- ikkita jadvalni birlashtirish orqali yangi episode reting jadvalini hosil qilndi ----------------------

    with st.expander('Ikkita jadvalni birlashtirib yangi jadval hosil qilish'):
        code = """
        data = df.join(  df1[['currentRank', 'node.titleType.text', 'node.releaseYear.endYear', 'node.ratingsSummary.aggregateRating',
            'node.ratingsSummary.voteCount', 'node.runtime.seconds', 'node.titleGenres.genres', 'node.id']].set_index('node.id'), on='series.id')    
            episode_count = data.groupby('title').count()['episode']

        numeric_columns = ['aggregateRating', 'node.ratingsSummary.aggregateRating', 'currentRank',
        'node.ratingsSummary.voteCount', 'voteCount']
        view = data.groupby(['series.id', 'title', 'node.titleType.text'])[numeric_columns].mean().round(1).sort_values('voteCount', ascending=False).copy()

        view = view.reset_index()

        view = view.join(episode_count, on='title')
            """
        st.code(code, language='python')

    data = df.join(
    df1[['currentRank', 'node.titleType.text', 'node.releaseYear.endYear', 'node.ratingsSummary.aggregateRating',	'node.ratingsSummary.voteCount', 'node.runtime.seconds', 'node.titleGenres.genres', 'node.id']].set_index('node.id'), on='series.id'
    )    
    episode_count = data.groupby('title').count()['episode']


    numeric_columns = ['aggregateRating', 'node.ratingsSummary.aggregateRating', 'currentRank', 'node.ratingsSummary.voteCount', 'voteCount']
    view = data.groupby(['series.id', 'title', 'node.titleType.text'])[numeric_columns].mean().round(1).sort_values('voteCount', ascending=False).copy()

    view = view.reset_index()

    view = view.join(episode_count, on='title')


    df1.set_index('node.id', inplace=True)

    columns_to_join = ['node.runtime.seconds', 'node.titleGenres.genres', 'node.releaseYear.year', 'node.releaseYear.endYear']
    view = view.join(df1[columns_to_join], on='series.id')


    view['url'] = view['series.id'].apply(lambda x: 'https://www.imdb.com/title/'+x)

    data = data[['currentRank', 'title', 'season',	'episode', 'node.titleType.text', 'aggregateRating', 'voteCount','node.ratingsSummary.aggregateRating', 'node.ratingsSummary.voteCount', 'node.runtime.seconds', 'node.titleGenres.genres', 'releaseDate.day', 'releaseDate.month', 'releaseDate.year']].sort_values('currentRank').reset_index(drop=True)
    view = view[['currentRank', 'title', 'episode', 'node.titleType.text', 'aggregateRating', 'voteCount', 'node.ratingsSummary.aggregateRating', 'node.ratingsSummary.voteCount', 'node.runtime.seconds', 'node.titleGenres.genres', 'node.releaseYear.year', 'node.releaseYear.endYear', 'url']].sort_values('currentRank').reset_index(drop=True)
    
    
    #-------------  Global reyting jadvalini ustunlarni nomi o'zgartitdim  va null qiymatlarni toldirdim -------------------
    
    with st.expander('Ustunlar nomini o\'zgartirish'):
        code = """
        rename_cols_ep = {
        'currentRank': 'Imdb Rank',
        'title': 'Title',
        'episode': 'Total Episode',
        'node.titleType.text': 'Type',
        'aggregateRating': 'Mean Episode Rating',
        'voteCount': 'Mean Episode Rating Count',
        'node.ratingsSummary.aggregateRating': 'Global Rating',
        'node.ratingsSummary.voteCount': 'Global Rating Count',
        'node.runtime.seconds': 'Duration (min)',
        'node.titleGenres.genres': 'Genres',
        'node.releaseYear.year': 'Start Year',
        'node.releaseYear.endYear': 'End Year'
        }
        view = view.rename(rename_cols_ep, axis=1)
        """
        st.code(code, language='python')
    
    rename_cols_ep = {
    'currentRank': 'Imdb Rank',
    'title': 'Title',
    'episode': 'Total Episode',
    'node.titleType.text': 'Type',
    'aggregateRating': 'Mean Episode Rating',
    'voteCount': 'Mean Episode Rating Count',
    'node.ratingsSummary.aggregateRating': 'Global Rating',
    'node.ratingsSummary.voteCount': 'Global Rating Count',
    'node.runtime.seconds': 'Duration (min)',
    'node.titleGenres.genres': 'Genres',
    'node.releaseYear.year': 'Start Year',
    'node.releaseYear.endYear': 'End Year'
    }
    view = view.rename(rename_cols_ep, axis=1)
    
    # --------------null qiymat o'rniga 2050 qoyishimga sabab bu serillar suratga olish hali tugamagan ----------------------
    view['End Year'] = view['End Year'].fillna(2050)



    # ----------------episode rating jadvalni ustunlar nomini o'zgartirib null qiymatlar o'rniga yillarga nisbatan grupirovga qilib o'rtacha qiymatini qo'ydim ----------------------
    rename_cols_ep = {
    'currentRank': 'Imdb Rank',
    'title': 'Title',
    'season':'Season',
    'episode': 'Episode',
    'node.titleType.text': 'Type',
    'aggregateRating': 'Episode Rating',
    'voteCount': 'Episode Rating Count',
    'node.ratingsSummary.aggregateRating': 'Global Series Rating',
    'node.ratingsSummary.voteCount': 'Global Rating Count',
    'node.runtime.seconds': 'Duration (min)',
    'node.titleGenres.genres': 'Genres',
    'releaseDate.day': 'Day',
    'releaseDate.month':'Month',
    'releaseDate.year':'Year'
    }

    data = data.rename(rename_cols_ep, axis=1)

    data['Day'] = data['Day'].fillna(35)
    data['Month'] = data['Month'].fillna(15)
    data['Year'] = data['Year'].fillna(2050)

    data['Episode Rating'] = data.groupby('Year')['Episode Rating'].transform(lambda x: x.fillna(round(x.mean(), 1)))
    data['Episode Rating'] = data.groupby('Month')['Episode Rating'].transform(lambda x: x.fillna(round(x.mean(), 1)))

    
    

    st.header('IMDb top 250ta seriyallarni epizodlar reytingi')
    st.dataframe(data) 
    # st.header('IMDb top 250ta seriyallarni global reytingi') 
    # st.dataframe(view)
# -----------------------------------------------------------------------------------------------------------------------------------------------

def page_2():
    st.title("Eng so'nggi IMDb(Internet film bazasi)dagi Top 250ta seriyallarni epizodlar reytinglari va seriyallarni global reytingi tahlili")
    
    with st.sidebar:
        multiselect = st.multiselect(
            "Janrlar o'zizga yoqganini tanglang:",
            genres , default='Documentary'
        )
        slider_global = st.slider('Global Reytingni tanlang:', min_value=min(global_retings), max_value=max(global_retings), value=[min(global_retings), max(global_retings)])

        slider_year = st.slider('Yillar oralig\'ini tanlang:', min_value=min(year), max_value=max(year), value=[min(year), max(year)])
    
    if multiselect:
        mask = view['Genres'].apply(lambda x: any(genre in x.split(' ,') for genre in multiselect))
        view1 = view[mask]
        data1 = data[data['Genres'].apply(lambda x: any(genre in x.split(' ,') for genre in multiselect))]
    
    view1 = view1[(view1['Global Rating'] >= slider_global[0]) & (view1['Global Rating'] <= slider_global[1])]
    view1 = view1[(view1['Start Year'] >= slider_year[0]) & (view1['Start Year'] <= slider_year[1])]

    data1 = data1[(data1['Global Series Rating'] >= slider_global[0]) & (data1['Global Series Rating'] <= slider_global[1])]
    data1 = data1[(data1['Year'] >= slider_year[0]) & (data1['Year'] <= slider_year[1])]

    dct = view1.groupby('Type')['Type'].count().to_dict()
    fig, ax =plt.subplots()




    
    
    st.line_chart(view1,
                y=['Global Rating Count'],
                x='Global Rating',
                )
    
    st.line_chart(view1,
                y=['Mean Episode Rating Count'],
                x='Mean Episode Rating',
                )
    
    select_box = st.selectbox('Grafik turini tanlang:',['Lmplot', 'Pie chart', 'Histplot', 'Scatterplot', 'Heatmap'])

    if select_box == 'Pie chart':
        ax.pie(list(dct.values()), labels=list(dct.keys()), autopct='%1.1f%%')
        st.pyplot(plt)

    elif select_box == 'Lmplot': 
    
        sns.set_style('whitegrid')
        g = sns.lmplot(
        data=view1,
        x="Mean Episode Rating", y="Global Rating", hue="Type"
        )
        st.pyplot(plt)
    

        sns.set_style('whitegrid')
        g = sns.lmplot(
        data=view1,
        x="Mean Episode Rating Count", y="Global Rating Count", hue="Type"
        )
        st.pyplot(plt)
    


    elif select_box == 'Histplot':

        fig, ax = plt.subplots()
        sns.histplot(view1['Global Rating'], bins=20, kde=True, color='skyblue', ax=ax)
        ax.set_title('Histogram of Global Ratings')
        ax.set_xlabel('Global Rating')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

        fig, ax = plt.subplots()
        sns.histplot(view1['Mean Episode Rating'], bins=20, kde=True, color='lightgreen', ax=ax)
        ax.set_title('Histogram of Mean Episode Ratings')
        ax.set_xlabel('Mean Episode Rating')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

        fig, ax = plt.subplots()
        sns.histplot(view1['Duration (min)'], bins=20, kde=True, color='salmon', ax=ax)
        ax.set_title('Histogram of Duration (min)')
        ax.set_xlabel('Duration (min)')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

    

    elif select_box == 'Scatterplot':

        fig, ax = plt.subplots()
        sns.scatterplot(x='Start Year', y='Mean Episode Rating', hue='Type', data=view1, palette="deep", ax=ax)
        ax.set_title('Scatterplot of Mean Episode Ratings by Start Year')
        ax.set_xlabel('Start Year')
        ax.set_ylabel('Mean Episode Rating')
        st.pyplot(fig)

        fig, ax = plt.subplots()
        sns.scatterplot(x='Start Year', y='Global Rating', hue='Type', data=view1, palette="deep", ax=ax)
        ax.set_title('Scatterplot of Global Rating by Start Year')
        ax.set_xlabel('Start Year')
        ax.set_ylabel('Global Rating')
        st.pyplot(fig)


        fig, ax = plt.subplots()
        sns.scatterplot(x='Year', y='Episode Rating', hue='Type', data=data1, palette="deep", ax=ax)
        ax.set_title('Scatterplot of Episode Ratings by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Episode Rating')
        st.pyplot(fig)

    elif select_box == 'Heatmap':
        corr = view1[['Global Rating', 'Mean Episode Rating', 'Global Rating Count', 'Mean Episode Rating Count', 'Duration (min)']].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, cbar_kws={"shrink": .5})
        ax.set_title('Heatmap of Correlations')
        st.pyplot(fig)

        # Pairplot
        fig = sns.pairplot(view1[['Global Rating', 'Mean Episode Rating', 'Duration (min)', 'Type']], hue='Type', palette='bright')
        st.pyplot(fig)
    







st.sidebar.title("Static site generators")



# -------------------------------------------- Sahifalar -----------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = "Sahifa 1"


if st.sidebar.button("Data Clear"):
    st.session_state.page = "Sahifa 1"
if st.sidebar.button("Data Analytics"):
    st.session_state.page = "Sahifa 2"



# Tanlangan sahifaga o'tish
if st.session_state.page == "Sahifa 1":
    page_1()
elif st.session_state.page == "Sahifa 2":
    page_2()


