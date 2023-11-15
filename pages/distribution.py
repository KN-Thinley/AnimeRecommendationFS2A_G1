import pandas as pd
import dash
from dash import html, dcc, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path="/distribution", name="Distribution")

anime = pd.read_csv("anime_cleaned.csv")
genre = anime['Genres'].str.split(', ', expand=True)
stacked_genres = genre.stack()
counts = stacked_genres.value_counts()

anime_counts = anime.shape[0]
average_score = anime['Score'].mean().__round__(2)
average_members = anime['Members'].mean().__round__(0)
average_episodes = anime['Episodes'].mean().__round__(0)
unique_genres = counts.nunique()



def create_distribution(col_name="Score"):
    return px.histogram(anime, x=col_name, nbins=20, color_discrete_sequence=["#ee8a1b"])

columns = ["Members", "Episodes", "Type", "Favorites"]
dd = dcc.Dropdown(id="dist_column", options=columns, value="Score", clearable=False)

# Add a dropdown for visualization type
visualization_dropdown = dcc.Dropdown(
    id='visualization_type',
    options=[
        {'label': 'Pie Chart', 'value': 'pie'},
        {'label': 'Bar Chart', 'value': 'bar'},
        {'label': 'Line Chart', 'value': 'line'},  
    ],
    value='pie',
    clearable=False
)

layout = html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                html.H1("Summary", className="text-4xl font-bold underline uppercase", style={"color": "#ee8a1b"}),
                html.Div(children=[
                    html.Div(children=[
                        html.H1("Anime Count", className="text-2xl font-bold text-center"),
                        html.H1(anime_counts, className="text-2xl text-center")
                    ]),
                    html.Div(children=[
                        html.H1("Average Score", className="text-2xl font-bold text-center"),
                        html.H1(average_score, className="text-2xl text-center")
                    ]),
                    html.Div(children=[
                        html.Div(children=[
                            html.H1("Average Members", className="text-2xl font-bold text-center"),
                            html.H1(average_members, className="text-2xl text-center")
                        ])
                    ]),
                    html.Div(children=[
                        html.Div(children=[
                            html.H1("Average Episodes", className="text-2xl font-bold text-center"),
                            html.H1(average_episodes, className="text-2xl text-center")
                        ])
                    ]),
                    html.Div(children=[
                        html.Div(children=[
                            html.H1("Unique Genres", className="text-2xl font-bold text-center"),
                            html.H1(unique_genres, className="text-2xl text-center")
                        ])
                    ]),
                ], className="flex justify-center items-center gap-8 pt-8"),
            ], className="flex flex-col justify-center items-center py-12 "),
    html.Div(children=[
        html.H1("General Distribution", className="text-2xl font-bold uppercase underline", style={"color": "#ee8a1b"}),
    ], className="p-4 rounded-sm"),
    html.Div(children=[
        html.Div(children=[
            html.H1("Genre Density in Anime", className="text-lg font-bold text-center"),
            dcc.Graph(id='genre-density-graph'),
        ], className="w-1/2 rounded-sm p-4"),
        html.Div(children=[
            html.H1("Top 5 Genre Distribution", className="text-lg font-bold text-center pb-4"),
            html.Div(visualization_dropdown, className="w-1/2"),
            dcc.Graph(id='top-5-genre-chart'),
            html.P("The genre with the most anime is Comedy with count of 6029 followed by Action with 3888 animes.")
        ], className="w-1/2 rounded-sm p-4"),
    ], className="flex justify-center items-center pt-8"),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H1("Select a column to view its distribution", className="text-lg font-bold text-start"),
                html.Div(
                    dd, className="w-1/2"
                )
            ], className="w-full rounded-sm"),
            dcc.Graph(id='histogram'),
        ], className="w-full bg-white rounded-sm"),
    ], className="flex justify-center items-center gap-8 p-8"),
                ], className="bg-white rounded-md")
], className="p-8")

@callback(Output("histogram", "figure"), [Input("dist_column", "value")])
def update_histogram(col_name):
    return create_distribution(col_name)

@callback(
    Output('genre-density-graph', 'figure'),
    [Input('dist_column', 'value')]
)
def update_density_bar_chart(id):
    fig = px.histogram(
        counts,
        x=counts.index,
        y=counts.values,
        color=counts.index,
        color_discrete_sequence=["#65d7b7", "#808af5", "#5c65c4", "#c18af5", "#ff712d"],
        nbins=20,  # Number of bins
    )
    fig.update_xaxes(title_text="Genre Types", tickangle=45)
    fig.update_yaxes(title_text="Counts")
    return fig

@callback(
    Output('top-5-genre-chart', 'figure'),
    [Input('top-5-genre-chart', 'id'),
     Input('visualization_type', 'value')]  # Added the dropdown input
)
def update_top_5_chart(id, visualization_type):
    top_5_genres = counts.head(5)
    
    if visualization_type == 'pie':
        fig = px.pie(top_5_genres, values=top_5_genres.values, names=top_5_genres.index, title="Top 5 Anime Genres",
                     color_discrete_sequence=["#65d7b7", "#808af5", "#5c65c4", "#c18af5", "#ff712d"])
        fig.update_traces(hole=0.4)
        total_entries = top_5_genres.values.sum()
        total =counts.values.sum()

# Adding annotation in the center with the total number of entries
        fig.add_annotation(
            text=f"{total_entries}/",
            x=0.5,
            y=0.55,
            showarrow=False,
            font=dict(size=15)
        )
        fig.add_annotation(
            text=f"{total}",
            x=0.5,
            y=0.49,
            showarrow=False,
            font=dict(size=20)
        )
    elif visualization_type == 'bar':
        fig = px.bar(
            top_5_genres,
            x=top_5_genres.index,
            y=top_5_genres.values,
            labels={'x': 'Anime Genres', 'y': 'Counts'},
            color=top_5_genres.index,
            color_discrete_sequence=["#65d7b7", "#808af5", "#5c65c4", "#c18af5", "#ff712d"]
        )
        fig.update_xaxes(title_text="Genre Types",tickangle=45)
        fig.update_yaxes(title_text="Counts")
    elif visualization_type == 'line':
        fig = px.line(
            top_5_genres.reset_index(name='Counts'),
            x=top_5_genres.index,
            y=top_5_genres.values,
            markers=True,
            color_discrete_sequence=["#ee8a1b"],
            title='Top 5 Anime Genres - Line Chart',
        )
        fig.update_xaxes(title_text="Genre Types",tickangle=45)
        fig.update_yaxes(title_text="Counts")
    
    return fig
