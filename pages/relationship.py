import pandas as pd
import dash 
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

dash.register_page(__name__, path="/relationship", name="Relationship")

anime = pd.read_csv("anime_cleaned.csv")

genre = anime['Genres'].str.split(', ', expand=True)
stacked_genres = genre.stack()
counts = stacked_genres.value_counts()
counts

anime['Genres'] = anime['Genres'].str.split(', ')
genre_df = anime.explode('Genres')

genre_popularity = genre_df.groupby('Genres')['Popularity'].mean().reset_index()
genre_audience = genre_df.groupby('Genres')['Members'].mean().reset_index()
merged_df = pd.merge(genre_popularity, genre_audience, on='Genres', suffixes=('_popularity', '_audience'))


fig = px.scatter(
    merged_df,
    x='Popularity',
    y='Members',
    text=merged_df['Genres'],
    labels={'Popularity': 'Average Popularity', 'Members': 'Average Members'},
    title='Genre Popularity vs. Audience',
)

fig.update_traces(
    mode='markers+text',
    marker=dict(size=10, opacity=0.7),
    textposition='bottom center',
    textfont=dict(size=12, color='black')
)

fig.update_layout(
    yaxis_title="Members"
)


question1 = px.bar(
    merged_df,
    x='Genres',
    y='Popularity',
    labels={'Popularity': 'Average Popularity', 'Members': 'Average Members'},
    title='Genre Vs Popularity',
    color="Genres",
)
anime['Genres'] = anime['Genres'].astype(str)

# Splitting the genres into separate columns
genre = anime['Genres'].str.split(', ', expand=True)
anime_with_genres = pd.concat([anime, genre], axis=1)

# Finding the top 5 anime with highest popularity in the 'Harem' genre
harem_anime = anime_with_genres[
    anime_with_genres.iloc[:, :6].apply(lambda row: any('Harem' in str(cell) for cell in row), axis=1)
]
harem_anime = harem_anime.sort_values(by='Popularity', ascending=True).head(5)

harem_anime_name = px.bar(
    harem_anime,
    x='Name',
    y='Popularity',
    labels={'Popularity': 'Popularity', 'Name': 'Anime Name'},
    title="Top 5 Harem Anime by Popularity"
)

question2 = px.bar(
    merged_df,
    x='Genres',
    y='Popularity',
    labels={'Genre': 'Genres', 'Score': 'Average Score '},
    title='Genre Vs Score',
    color="Genres",
)

question2.update_yaxes(title_text="Average Score")

thriller_anime = anime_with_genres[
    anime_with_genres.iloc[:, :6].apply(lambda row: any('Thriller' in str(cell) for cell in row), axis=1)
]
thriller_anime = thriller_anime.sort_values(by='Score', ascending=False).head(5)
print(thriller_anime)

thriller_anime_name = px.bar(
    thriller_anime,
    x='Name',
    y='Score',
    labels={'Score': ' Score', 'Name': 'Anime Name'},
    title="Top 5 Thriller Anime by Score"
)


correlation = anime['Score'].corr(anime['Popularity'])
episodeCorrelation = anime['Episodes'].corr(anime['Popularity'])

scorePopularity = px.scatter(
    anime, 
    x='Score',
    y='Popularity',
    title=f"Correlation between Score and Popularity: {correlation}",
    color_discrete_sequence=["#ee8a1b"],
)

episodePopularity = px.scatter(
    anime, 
    x="Episodes",
    y="Popularity",
    title=f"Correlation between Episodes and Popularity: {episodeCorrelation}",
    color_discrete_sequence=["#ee8a1b"]
)


anime_less_than_20 = anime[anime['Episodes'] < 20].nsmallest(10, 'Popularity')
less_than_20 = px.bar(
    anime_less_than_20,
    x='Name',
    y='Popularity',
    color="Name",
    labels={'Popularity': ' Popularity Ranking', 'Name': 'Anime Name'},
    title="Top Animes with less than 20 Episodes by Popularity"
)

anime_less_than_50 = anime[(anime['Episodes'] > 20) & (anime['Episodes'] < 50)].nsmallest(10, 'Popularity')
anime_less_than_50 = px.bar(
    anime_less_than_50,
    x='Name',
    y='Popularity',
    color="Name",
    labels={'Popularity': ' Popularity Ranking', 'Name': 'Anime Name'},
    title="Top Animes with less than 50 Episodes by Popularity"
)

anime_less_than_100 = anime[(anime['Episodes'] > 50) & (anime['Episodes'] < 100)].nsmallest(10, 'Popularity')
anime_less_than_100 = px.bar(
    anime_less_than_100,
    x='Name',
    y='Popularity',
    color="Name",
    labels={'Popularity': ' Popularity Ranking', 'Name': 'Anime Name'},
    title="Top Animes with less than 100 Episodes by Popularity"
)

anime_greater_than_100 = anime[anime['Episodes'] > 100].nsmallest(10, 'Popularity')
anime_greater_than_100 = px.bar(
    anime_greater_than_100,
    x='Name',
    y='Popularity',
    color="Name",
    labels={'Popularity': ' Popularity Ranking', 'Name': 'Anime Name'},
    title="Top Animes with more than 100 Episodes by Popularity"
)

topPopularity = anime.sort_values(by="Popularity", ascending=True)

topPopularity_anime = topPopularity.head(10)

topPopularity = px.bar(
    topPopularity_anime,
    x='Name',
    y='Popularity',
    color="Name",
    labels={'Populariy': ' Popularity Ranking', 'Name': 'Anime Name'},
    title="Top Animes by Popularity"
)


topScore = anime.sort_values(by="Score", ascending=False)
topScore_anime = topScore.head(10)

topScore = px.bar(
    topScore_anime,
    x='Name',
    y='Score',
    color="Name",
    labels={'Score': ' Score', 'Name': 'Anime Name'},
    title="Top Animes by Score"
)

anime_data = pd.read_csv('anime_cleaned.csv')
anime_data['Genres'] = anime_data['Genres'].str.split(', ')
genre_df = anime_data.explode('Genres')
genre_audience = genre_df.groupby('Genres')['Members'].mean().reset_index()
genre_audience = genre_audience.sort_values(by='Members', ascending=False)

top_genres = genre_audience

genre_audience = px.bar(
    top_genres,
    x='Genres',
    y='Members',
    color="Genres",
    labels={'Members': 'Average Members', 'Genres': 'Genre'},
    title="Top Genres by Members"
)

thriller_anime_audience = anime_with_genres[
    anime_with_genres.iloc[:, :6].apply(lambda row: any('Thriller' in str(cell) for cell in row), axis=1)
]
thriller_anime_audience = thriller_anime_audience.sort_values(by='Members', ascending=False).head(5)

thriller_anime_audience = px.bar(
    thriller_anime_audience,
    x='Name',
    y='Members',
    color="Name",
    labels={'Members': ' Members', 'Name': 'Anime Name'},
    title="Top 5 Thriller Anime by Members"
)


def create_scatter_chart(x_axis="Score", y_axis="Members"):
    return px.scatter(anime, x=x_axis, y=y_axis, height=600)

columns = ["Score", "Members", "Episodes", "Type", "Favorites", "Aired Year",]
x_axis = dcc.Dropdown(id="x_axis", options=columns, value="Score", clearable=False)
y_axis = dcc.Dropdown(id="y_axis", options=columns, value="Members", clearable=False)


score_bins = [0, 2, 4, 6, 8, 10]
score_labels = ['0-2', '2-4', '4-6', '6-8', '8-10']
member_bins = [0, 5000, 10000, 50000, 100000, 500000, float('inf')]
member_labels = ['0-5k', '5k-10k', '10k-50k', '50k-100k', '100k-500k', '500k+']

anime['Score_Range'] = pd.cut(anime['Score'], bins=score_bins, labels=score_labels)
anime['Members_Range'] = pd.cut(anime['Members'], bins=member_bins, labels=member_labels)

genre_data = anime.explode('Genres')
average_genre_data = genre_data.groupby('Genres').agg({'Score': 'mean', 'Members': 'mean'}).reset_index()

sankey = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=score_labels + member_labels
    ),
    link=dict(
        source=[0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
        target=[5, 6, 5, 6, 7, 8, 7, 8, 9, 10],
        value=average_genre_data['Score'].tolist() + average_genre_data['Members'].tolist()
    )
))

sankey.update_layout(title_text="Sankey Diagram for Score, and Members")


layout = html.Div(children=[
    html.Div(children=[
        html.Div([
            



        html.Div(children=[
            html.H1("Question 1: How does the genre of an anime affect it's popularity among viewers?", className="text-2xl font-bold underline uppercase", style={"color": "#ee8a1b"}),
            dcc.Graph(figure=question1),
            html.P("*Note that the Popularity here refers to the average popularity ranking which defines the lower numerical value being higher in terms of popularity ranking.", className="font-bold pb-4"),

            html.H1("Recommendations", className="text-xl font-bold uppercase pb-4", style={"color": "#ee8a1b"}),
            html.Div(children=[
                html.H1("Choose Options"),
                dcc.RadioItems(
                    id='harem_top_n_selection',
                    options=[
                        {'label': 'Top 5', 'value': 5},
                        {'label': 'Top 10', 'value': 10},
                        {'label': 'Top 20', 'value': 20}
                    ],
                    value=5,
                    className="flex gap-4"
                ),
                dcc.Graph(id='harem_anime_name')
            ]),
        ]),


        html.Div(children=[
            html.H1("Question 2: Is there a correlation between the rating of an anime and its popularity?" , className="text-2xl font-bold underline uppercase py-8", style={"color": "#ee8a1b"}),
            dcc.Graph(figure=scorePopularity),

            html.H1("Recommendations" , className="text-xl font-bold uppercase pb-4", style={"color": "#ee8a1b"}),
            html.Div(children=[
                dcc.Graph(figure=topPopularity),
            dcc.Graph(figure=topScore),
            ], className="flex")
        ]),

        html.Div(children=[
            html.H1("Question 3: Does the number of episodes in anime impact its popularity?" , className="text-2xl font-bold underline uppercase py-8", style={"color": "#ee8a1b"}),
            dcc.Graph(figure=episodePopularity),

            html.H1("Recommendations",  className="text-xl font-bold uppercase pb-4", style={"color": "#ee8a1b"}),
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(figure=less_than_20),
                    dcc.Graph(figure=anime_less_than_50),
                ], className="flex"),
                html.Div(children=[
                    dcc.Graph(figure=anime_less_than_100),
                    dcc.Graph(figure=anime_greater_than_100),
                ], className="flex")
            ], className="flex flex-col gap-4")
        ]),

        html.Div(children=[
            html.H1("Question 4: Are there any specific genres that consistently attract higher audience?" , className="text-2xl font-bold underline uppercase py-8", style={"color": "#ee8a1b"}),
            dcc.Graph(figure=genre_audience),

            html.H1("Recommendations",  className="text-xl font-bold uppercase pb-4", style={"color": "#ee8a1b"}),
            dcc.Graph(figure=thriller_anime_audience),
        ]),

        html.Div(children=[
            html.H1("Question 5: Are there any specific genres that tends to have higher ratings?" , className="text-2xl font-bold underline uppercase py-8", style={"color": "#ee8a1b"}),
            dcc.Graph(figure=question2),
            html.H1("Recommendations",  className="text-xl font-bold uppercase pb-4", style={"color": "#ee8a1b"}),
            html.Div(children=[
                html.H1("Choose Options"),
                dcc.RadioItems(
                    id='thriller_top_n_selection',
                    options=[
                        {'label': 'Top 5', 'value': 5},
                        {'label': 'Top 10', 'value': 10},
                        {'label': 'Top 20', 'value': 20}
                    ],
                    value=5,
                    className="flex gap-4"
                ),
                dcc.Graph(id='thriller_anime_name')
            ]),
        ]),
        html.H1("Other Relationships", className="text-2xl font-bold underline uppercase py-8", style={"color": "#ee8a1b"}),
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.H1("Select X-Axis"),
                    x_axis,
                ]),
                html.Div(children=[
                    html.H1("Select Y-Axis"),
                    y_axis,
                ]),
            ], className="flex w-full gap-4"),
        dcc.Graph(id="scatter_chart"),

        html.H1("Genre Popularity vs. Audience"),
            dcc.Graph(figure=fig),
            html.Div([
                dcc.Graph(figure=sankey),
            ]),
    ]),
  
     ])
    ], className="bg-white rounded-md p-8")
], className="p-8")

@callback(Output("scatter_chart", "figure"), [Input("x_axis", "value"), Input("y_axis", "value")])
def update_scatter_chart(x_axis, y_axis):
    return create_scatter_chart(x_axis, y_axis)

@callback(
    Output('harem_anime_name', 'figure'),
    Input('harem_top_n_selection', 'value')
)
def update_harem_anime_name(selected_value):
    harem_anime_filtered = anime_with_genres[
        anime_with_genres.iloc[:, :6].apply(lambda row: any('Harem' in str(cell) for cell in row), axis=1)
    ]
    harem_anime_filtered = harem_anime_filtered.sort_values(by='Popularity', ascending=True).head(selected_value)

    updated_figure = px.bar(
        harem_anime_filtered,
        x='Name',
        y='Popularity',
        labels={'Popularity': 'Popularity', 'Name': 'Anime Name'},
        color="Name",
        title=f"Top {selected_value} Harem Anime by Popularity"
    )
    
    return updated_figure

@callback(
    Output('thriller_anime_name', 'figure'),
    Input('thriller_top_n_selection', 'value')
)
def update_thriller_anime_name(selected_value):
    thriller_anime_filtered = anime_with_genres[
        anime_with_genres.iloc[:, :6].apply(lambda row: any('Thriller' in str(cell) for cell in row), axis=1)
    ]
    thriller_anime_filtered = thriller_anime_filtered.sort_values(by='Score', ascending=False).head(selected_value)

    updated_figure = px.bar(
        thriller_anime_filtered,
        x='Name',
        y='Score',
        labels={'Score': ' Score', 'Name': 'Anime Name'},
        color="Name",
        title=f"Top {selected_value} Thriller Anime by Score"
    )
    
    return updated_figure


# For subplots related to episodes vs. popularity
episodePopularity.update_layout(xaxis_tickangle=-45)
less_than_20.update_layout(xaxis_tickangle=-45)
anime_less_than_50.update_layout(xaxis_tickangle=-45)
anime_less_than_100.update_layout(xaxis_tickangle=-45)
anime_greater_than_100.update_layout(xaxis_tickangle=-45)

# Other subplots
# Set the x-axis label angle to 45 degrees for consistency
topPopularity.update_layout(xaxis_tickangle=-45)
topScore.update_layout(xaxis_tickangle=-45)
genre_audience.update_layout(xaxis_tickangle=-45)
thriller_anime_audience.update_layout(xaxis_tickangle=-45)
question2.update_layout(xaxis_tickangle=-45)
