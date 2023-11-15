import dash
from dash import html, dcc 
import pandas as pd

dash.register_page(__name__, path="/", name = "Home")

anime = pd.read_csv("anime_cleaned.csv")

layout = html.Div(children=[
    html.Div(children=[
        html.Img(src="./static/herobanner.png", className=""),
        html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H1("Project Overview", className="text-4xl font-bold underline uppercase", style={"color": "#ee8a1b"}),
                    html.P("Our data visualization project revolves around extracting insights from a rich dataset sourced from MyAnimeList, the go-to platform for anime enthusiasts. We have analyzed the data to address five key research questions, offering a comprehensive view of the anime landscape. This dashboard serves as a gateway to explore the fascinating findings we've uncovered through our exploration of the dataset.", className="pt-4 text-2xl text-justify  ")
                ], className="pl-12 pr-48 w-3/5 pt-12"),
                html.Img(src="./static/details.png", className="w-2/5 rounded-md", style={"border": "4px solid #ee8a1b"})
            ], className="flex"),
            html.Div([
                html.Img(src="./static/details2.png", className="w-3/5 rounded-md", style={"border": "4px solid #ee8a1b"}),
                html.Div([
                    html.H1("Research Questions", className="text-4xl font-bold underline uppercase", style={"color": "#ee8a1b"}),
                    html.P("1: How does the genre of an anime affect it's popularity among viewers?", className="pt-4 text-xl text-justify"),
                    html.P("2: Is there a correlation between the rating of an anime and its popularity?", className="pt-4 text-xl text-justify"),
                    html.P("3: Does the number of episodes in anime impact its popularity?", className="pt-4 text-xl text-justify"),
                    html.P("4: Are there any specific genres that consistently attract higher audience?", className="pt-4 text-xl text-justify"),
                    html.P("5: Are there any specific genres that tends to have higher ratings?", className="pt-4 text-xl text-justify"),
                ], className="pr-12 pl-16 w-2/5"),
            ], className="flex pt-12"),
            html.Div(children=[
                dcc.Link("Dashboard →", className="text-lg text-center uppercase px-5 py-2 text-white rounded-sm", style={"background": "#ee8a1b"}, href="/relationship")
            ], className="w-full pt-20 flex justify-center items-center")
        ], className="bg-white pb-4 rounded-md"),  
    ], className="px-8 pb-8"),
], className=""),

])