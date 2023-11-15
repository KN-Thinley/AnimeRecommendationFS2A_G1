from dash import Dash, html, dcc
import dash
import plotly.express as px

external_css = ["./styles.css","https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css", ]

app = Dash(__name__, pages_folder="pages", use_pages=True, external_stylesheets=external_css)

app.layout = html.Div([ 
    html.Div(children=[
        html.Div([
            dcc.Link(html.H1("Anime Recommendation", className="text-2xl text-center uppercase px-5 py-5 text-white", style={"background": "#ee8a1b"}), href="/"),
            
        ]),
        html.Div([
            dcc.Link("Distribution", href="/distribution", className="hover:underline"),
            dcc.Link("Recommendation", href="/relationship", className="hover:underline"),
        ], className="flex justify-center items-center text-lg uppercase font-bold text-white gap-4 pr-4", style={"color": "#ee8a1b"}),
    ], style={"border-bottom": "4px solid #ee8a1b"}, className="flex justify-between items-center shadow-md"),
    dash.page_container
], className="mx-auto background",
style={
    "font-family": "DIN",
    "background": "url(./static/tori.jpg) no-repeat fixed",
    "background-size": "cover"
}
)

if __name__ == "__main__":
    app.run(debug=True)
