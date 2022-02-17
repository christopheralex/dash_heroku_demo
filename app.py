import altair as alt
import pandas as pd
from dash import Dash, dcc, html, Input, Output
# alt.data_transformers.enable('data_server')
# alt.renderers.enable('mimetype')

    
df = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv")
columns = ["track_popularity", "liveness"]
df = df[columns]
df = df.sample(4500, random_state=123)


def plot_altair(xmax, data=df.copy()):
    chart = alt.Chart(data[data["track_popularity"] <= xmax]).mark_line().encode(
        x=alt.X('track_popularity',  bin=alt.Bin(maxbins=20)),
        y = "mean(liveness)")
    return chart.to_html()

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
        html.Iframe(
            id='scatter',
            srcDoc=plot_altair(xmax=0),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.Slider(id='xslider', value=50, min=0, max=100)])
        
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xslider', 'value'))
def update_output(xmax):
    return plot_altair(xmax)

if __name__ == '__main__':
    app.run_server(debug=True)
