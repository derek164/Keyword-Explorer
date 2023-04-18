import pandas as pd
import database as db
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html, MATCH, ALL

# from dash import dash_table

"""
https://img.icons8.com/material/24/045241/hand-drawn-star.png
https://img.icons8.com/material/24/759c93/hand-drawn-star.png
https://img.icons8.com/material-outlined/24/045241/hand-drawn-star.png
https://img.icons8.com/material-outlined/24/759c93/hand-drawn-star.png

['An Internet-wide view of ICS devices', 'IoT Data Prefetching in Indoor Navigation SOAs']
"""

gds = db.gds.Client(database="academicworld")
mysql = db.mysql.Client(database="academicworld")
mongo = db.mongo.Client(database="academicworld")
neo4j = db.neo4j.Client(database="academicworld")
prepared = db.prepared.Client(database="academicworld")


keywords = pd.DataFrame(mysql.execute(query=mysql.get_keywords))["name"].sort_values()


def get_most_relevant_publications(**kwargs):
    return [
        publication["title"]
        for publication in mysql.execute(
            query=mysql.get_most_relevant_publications, **kwargs
        )
    ]


def get_most_relevant_university(**kwargs):
    return [
        institute["institute"]
        for institute in neo4j.execute(
            query=neo4j.get_most_relevant_universities, **kwargs
        )
    ]


def get_favorites():
    return [
        favorite["title"] for favorite in prepared.execute(query=prepared.get_favorites)
    ]


def add_favorite(title):
    print("Adding favorite: " + title)
    prepared.execute(query=prepared.insert_favorite, tuple=(title,))


def remove_favorite(title):
    print("Removing favorite: " + title)
    prepared.execute(query=prepared.remove_favorite, tuple=(title,))


def generate_publication_list(publications):
    favorites = get_favorites()
    return [
        html.Div(
            children=[
                publication,
                html.Button(
                    id={"type": "publication-elem-button", "index": publication},
                    children=[
                        html.Img(
                            src="https://img.icons8.com/material/24/045241/hand-drawn-star.png"
                            if publication in favorites
                            else "https://img.icons8.com/material-outlined/24/045241/hand-drawn-star.png",
                            style={"height": "20px", "width": "20px"},
                        )
                    ],
                    n_clicks=0,
                    className="publication-elem-button",
                ),
            ],
            className="publication-elem",
        )
        for publication in publications
    ]


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
        html.Div(
            dcc.Tabs(
                id="publication-tabs",
                value="top-publications",
                children=[
                    dcc.Tab(
                        label="Top Publications",
                        value="top-publications",
                        className="tab-title",
                        selected_style={
                            "font-weight": "900",
                            "color": "#079A82",
                        },
                    ),
                    dcc.Tab(
                        label="University",
                        value="university",
                        className="tab-title",
                        selected_style={
                            "font-weight": "900",
                            "color": "#079A82",
                        },
                    ),
                    dcc.Tab(
                        label="Favorites",
                        value="favorites",
                        className="tab-title",
                        selected_style={
                            "font-weight": "900",
                            "color": "#079A82",
                        },
                    ),
                ],
            ),
            className="publications-tab",
        ),
        html.Div(
            id="publication-tabs-content",
            className="publications-card",
        ),
        # html.Div(
        #     # children=[
        #     #     # html.Div(children="Favorites", className="menu-title"),
        #     #     html.Div(children=generate_publication_list(get_favorites())),
        #     # ],
        #     children=[],
        #     id="favorites",
        #     className="publications-card",
        # ),
        # html.Div(
        #     children=[],
        #     id="top-publications",
        #     className="publications-card",
        # ),
        # html.Div(
        #     children=[
        #         html.H1(children="Hello Dash"),
        #         html.Div(children=[step()], id="step_list"),
        #         html.Button("Add Step", id="add_step_button", n_clicks_timestamp=0),
        #         html.Button("Remove Step", id="remove_step_button", n_clicks_timestamp=0),
        #     ]
        # )
    ]
)


@app.callback(
    Output("publication-tabs-content", "children"),
    Input("publication-tabs", "value"),
    Input("keyword-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def render_content(tab, keyword, start_date, end_date):
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])
    if tab == "top-publications":
        return html.Div(
            children=generate_publication_list(
                get_most_relevant_publications(
                    keyword=keyword, start_year=start_year, end_year=end_year
                )
            )
        )
    elif tab == "university":
        top_universities = get_most_relevant_university(
            keyword=keyword, start_year=start_year, end_year=end_year
        )
        print(top_universities)
        return html.Div(
            children=[
                dcc.Dropdown(
                    id="university-filter",
                    options=[
                        {"label": university, "value": university}
                        for university in top_universities
                    ],
                    value="Stanford University",
                    clearable=False,
                    className="dropdown",
                    style={"min-width": "1024px"}
                ),
            ]
        )
    elif tab == "favorites":
        favorites = get_favorites()
        return html.Div(children=generate_publication_list(favorites))


# @app.callback(
#     Output("top-publications", "children"),
#     Input("keyword-filter", "value"),
#     Input("date-range", "start_date"),
#     Input("date-range", "end_date"),
# )
# def update_top_publications(keyword, start_date, end_date):
#     start_year = int(start_date[:4])
#     end_year = int(end_date[:4])
#     return (
#         # html.Div(children="Favorites", className="menu-title"),
#         html.Div(
#             children=generate_publication_list(
#                 get_most_relevant_publications(
#                     keyword=keyword, start_year=start_year, end_year=end_year
#                 )
#             )
#         ),
#     )


# html.Div(
#     children=[
#         # html.Div(children="Favorites", className="menu-title"),
#         html.Div(children=generate_publication_list(get_favorites())),
#     ],
#     id="favorites",
#     className="publications-card",
# ),
# html.Div(
#     id="top-publications",
#     className="publications-card",
# ),

# children=[
#     # html.Div(children="Favorites", className="menu-title"),
#     html.Div(children=generate_publication_list(get_favorites())),
# ],
# id="favorites",

# @app.callback(
#     Output("favorites", "children"),
#     Input("top-publications", "children"),
#     # [Input({"type": "publication-elem-button", "index": MATCH}, "n_clicks")],
# )
# def sync_favorites(top_publications):
#     print("Syncing favorites table")
#     favorites = get_favorites()
#     return html.Div(children=generate_publication_list(favorites))

# @app.callback(
#     Output("favorites", "children"),
#     [Input({"type": "publication-elem-button", "index": ALL}, "n_clicks")],
# )
# def sync_favorites(n_clicks):
#     print("Syncing favorites table")
# favorites = get_favorites()
# return html.Div(children=generate_publication_list(favorites))


@app.callback(
    Output({"type": "publication-elem-button", "index": MATCH}, "children"),
    [Input({"type": "publication-elem-button", "index": MATCH}, "n_clicks")],
    [State({"type": "publication-elem-button", "index": MATCH}, "id")],
    [State({"type": "publication-elem-button", "index": MATCH}, "children")],
)
def update_publication_favorites(n_clicks, id, existing_state):
    if n_clicks == 0:
        return existing_state
    title = id["index"]
    favorites = get_favorites()
    favorited = title in favorites
    print((title, favorited, favorites))
    remove_favorite(title) if favorited else add_favorite(title)

    # favorites = html.Div(children=generate_publication_list(favorites))
    updated_button = html.Img(
        id={
            "type": "publication-elem-button-image",
            "index": id["index"],
        },
        src="https://img.icons8.com/material/24/045241/hand-drawn-star.png"
        if not favorited
        else "https://img.icons8.com/material-outlined/24/045241/hand-drawn-star.png",
        style={"height": "20px", "width": "20px"},
    )
    return updated_button


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


# @app.callback(
#     Output({'type': 'publication-elem-button-output', 'index': MATCH}, 'children'),
#     [Input({'type': 'publication-elem-button', 'index': MATCH}, 'n_clicks')],
#     [State({'type': 'publication-elem-button', 'index': MATCH}, 'id')],
# )
# def display_output(n_clicks, id):
#     return html.Div('n-clicks: {}, index: {}'.format(n_clicks, id['index']))

# def get_favorites():
#     return [favorite["title"] for favorite in prepared.execute(query=prepared.get_favorites)]

# def add_favorite(title):
#     prepared.execute(query=prepared.insert_favorite, tuple=(title,))

# def remove_favorite(title):
#     prepared.execute(query=prepared.remove_favorite, tuple=(title,))


if __name__ == "__main__":
    app.run_server(debug=True)
