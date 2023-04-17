import pandas as pd
import database as db
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html


gds = db.gds.Client(database="academicworld")
mysql = db.mysql.Client(database="academicworld")
mongo = db.mongo.Client(database="academicworld")
neo4j = db.neo4j.Client(database="academicworld")
prepared = db.prepared.Client(database="academicworld")


keywords = pd.DataFrame(mysql.execute(query=mysql.get_keywords))["name"].sort_values()


external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?" "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Keyword Explorer"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Keyword Explorer", className="header-title"),
                html.P(
                    children=(
                        "Learn about the who, what, and when of keywords "
                        "and save interesting publications to check out later!"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Keywords", className="menu-title"),
                        dcc.Dropdown(
                            id="keyword-filter",
                            options=[
                                {"label": keyword, "value": keyword}
                                for keyword in keywords
                            ],
                            value="internet",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Date Range", className="menu-title"),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed="1903-01-01",
                            max_date_allowed="2021-12-31",
                            start_date="2015-01-01",
                            end_date="2021-12-31",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                )
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    Input("keyword-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_price_chart(keyword, start_date, end_date):
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])
    test = pd.DataFrame(
        mongo.execute(
            query=mongo.get_citations_and_relevance_by_year,
            keyword=keyword,
            start_year=start_year,
            end_year=end_year,
        )
    )
    fig = go.Figure()
    fig.layout = {
        "title": {
            "text": "Number of Citatations and Relevance",
            "x": 0.05,
            "xanchor": "left",
        },
        "xaxis": {"fixedrange": True},
        "yaxis": {"fixedrange": True},
    }
    fig.add_trace(
        go.Scatter(
            x=test["year"],
            y=test["citations"],
            mode="lines+markers",
            name="Citations",
            hovertemplate="Citations: %{y:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=test["year"],
            y=test["relevance"],
            mode="lines+markers",
            name="Relevant Citations",
            hovertemplate="Relevant Citations: %{y:.2f}<extra></extra>",
        )
    )
    fig.update_layout(hovermode="x unified")
    fig.update_layout(xaxis=dict(tickmode="linear", tick0=start_year, dtick=1))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
