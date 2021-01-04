import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    
    html.Div(
        html.P(
            "wiki nearby articles",
            style = {
                "font-size": "72px",
                "fontFamily": "monospace",
                # "width": "100%",
                "text-align": "center"

            }
        
        )
    )
])

if __name__ == '__main__':
  app.run_server(debug=True, threaded=True)
