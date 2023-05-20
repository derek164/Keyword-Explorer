import time
from itertools import cycle
from pathlib import Path

import dash_loading_spinners as dls
import plotly.express as px
import plotly.graph_objects as go
from dash import ALL, MATCH, Dash, Input, Output, State, ctx, dcc, html, no_update
from dash.exceptions import PreventUpdate
from requests.utils import requote_uri

from api import KeywordAPI

client = KeywordAPI(database="academicworld")
expansion = Path(__file__).resolve().parent.joinpath("expansion")
keywords_cache = expansion.joinpath("keywords.txt")
keywords = open(keywords_cache).read().split("\n")


def generate_keywords_list(keywords):
    return [
        html.Button(
            id={
                "type": "keyword-button",
                "index": keyword,
            },
            children=[keyword],
            n_clicks=0,
            className="keyword-button",
        )
        for keyword in keywords
    ]


def generate_publication_list(publications):
    favorites = client.get_favorites()
    publications = [
        publication
        for publication in publications
        if client.publication_is_linked(publication)
    ]
    return [
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Button(
                            id={
                                "type": "publication-elem-button",
                                "index": publication,
                            },
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
                        html.A(
                            publication,
                            href=requote_uri(client.get_crossref_url(publication)),
                            className="publication-elem-link",
                            target="_blank",
                        ),
                    ],
                    className="publication-elem",
                ),
                html.Div(
                    children=generate_keywords_list(
                        client.get_publication_keywords(publication)
                    ),
                    className="keywords-container",
                ),
            ],
            className="publication-card",
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
            id="div-loading",
            children=[
                dls.Pacman(fullscreen=True, color="#435278", id="loading-whole-app")
            ],
        ),
        html.Div(
            className="div-app",
            id="div-app",
            children=html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H1(
                                children="Keyword Explorer", className="header-title"
                            ),
                            html.P(
                                children=(
                                    "Learn about the who, what, and when of the academic world "
                                    "and save interesting publications for later!"
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
                                    html.Div(
                                        children="Keywords", className="menu-title"
                                    ),
                                    dcc.Dropdown(
                                        id="keyword-filter",
                                        options=[
                                            {"label": keyword, "value": keyword}
                                            for keyword in keywords
                                        ],
                                        value="sql",
                                        # placeholder="Select a keyword",
                                        clearable=False,
                                        className="dropdown",
                                    ),
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children="Date Range", className="menu-title"
                                    ),
                                    dcc.DatePickerRange(
                                        id="date-range",
                                        min_date_allowed="1903-01-01",
                                        max_date_allowed="2021-12-31",
                                        start_date="2010-01-01",
                                        end_date="2021-12-31",
                                        style={
                                            "font-size": "4px",
                                            "display": "inline-block",
                                            "border-collapse": "separate",
                                        },
                                    ),
                                ]
                            ),
                        ],
                        className="menu",
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.Div(children=[], id="similar-keywords"),
                                ]
                            )
                        ],
                        className="summary",
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                # children=dls.Hash(
                                children=dls.Ellipsis(
                                    children=dcc.Graph(
                                        id="keyword-trend-chart",
                                        config={"displayModeBar": False},
                                    ),
                                    debounce=500,
                                    color="#435278",
                                    width=90,
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
                                    label="Top Universities",
                                    value="top-universities",
                                    className="tab-title",
                                    selected_style={
                                        "font-weight": "900",
                                        "color": "#079A82",
                                    },
                                ),
                                dcc.Tab(
                                    label="Top Researchers",
                                    value="top-researchers",
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
                        children=dls.Ellipsis(
                            children=html.Div(
                                id="publication-tabs-content",
                                className="publications-card",
                            ),
                            debounce=500,
                            show_initially=False,
                            color="#435278",
                            width=90,
                        ),
                        className="publications-wrapper",
                    ),
                ]
            ),
        ),
    ]
)


@app.callback(
    Output("div-loading", "children"),
    [Input("div-app", "loading_state")],
    [
        State("div-loading", "children"),
    ],
)
def hide_loading_after_startup(loading_state, children):
    # Sourced solution from Dash community:
    # https://community.plotly.com/t/show-a-full-screen-loading-spinner-on-app-start-up-then-remove-it/60174

    if children:
        time.sleep(2)  # to cover slow loading components
        print("remove loading spinner!")
        return None
    print("spinner already gone!")
    raise PreventUpdate


@app.callback(
    Output("similar-keywords", "children"),
    Input("keyword-filter", "value"),
)
def update_similar_keywords(keyword):
    keywords = client.get_similar_keywords(keyword=keyword)
    return html.Div(children=generate_keywords_list(keywords))


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
                client.get_most_relevant_publications(
                    keyword=keyword, start_year=start_year, end_year=end_year
                )
            )
        )
    elif tab == "top-universities":
        top_universities = client.get_most_relevant_university(
            keyword=keyword, start_year=start_year, end_year=end_year
        )
        return html.Div(
            children=[
                dcc.Dropdown(
                    id="university-filter",
                    options=[
                        {"label": university, "value": university}
                        for university in top_universities
                    ],
                    # value=top_universities[0],
                    placeholder="Select a university from the rankings",
                    clearable=False,
                    className="dropdown",
                    style={
                        "margin": "-1px auto 0 auto",
                        "border-bottom": "1px solid rgba(0, 0, 0, 0.18)",
                        "min-width": "1024px",
                        "height": "48px",
                        "font-weight": "500",
                    },
                ),
                html.Div(children=[], id="university-publications"),
            ]
        )
    elif tab == "top-researchers":
        top_researchers = client.get_most_relevant_faculty(
            keyword=keyword, start_year=start_year, end_year=end_year
        )
        return html.Div(
            children=[
                dcc.Dropdown(
                    id="researcher-filter",
                    options=[
                        {"label": researcher, "value": researcher}
                        for researcher in top_researchers
                    ],
                    # value=top_researchers[0],
                    placeholder="Select a researcher from the rankings",
                    clearable=False,
                    className="dropdown",
                    style={
                        "margin": "-1px auto 0 auto",
                        "border-bottom": "1px solid rgba(0, 0, 0, 0.18)",
                        "min-width": "1024px",
                        "height": "48px",
                        "font-weight": "500",
                    },
                ),
                html.Div(children=[], id="researcher-publications"),
            ]
        )
    elif tab == "favorites":
        favorites = client.get_favorites()
        return html.Div(children=generate_publication_list(favorites))


@app.callback(
    Output("university-publications", "children"),
    Input("university-filter", "value"),
    Input("keyword-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
    # prevent_initial_call=True,
)
def update_university_publications(university, keyword, start_date, end_date):
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])
    if university is None:
        return no_update
    return html.Div(
        children=generate_publication_list(
            client.get_most_relevant_university_publications(
                university=university,
                keyword=keyword,
                start_year=start_year,
                end_year=end_year,
            )
        )
    )


@app.callback(
    Output("researcher-publications", "children"),
    Input("researcher-filter", "value"),
    Input("keyword-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_researcher_publications(researcher, keyword, start_date, end_date):
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])
    if researcher is None:
        return no_update
    return html.Div(
        children=generate_publication_list(
            client.get_most_relevant_faculty_publications(
                faculty=researcher,
                keyword=keyword,
                start_year=start_year,
                end_year=end_year,
            )
        )
    )


@app.callback(
    Output("keyword-filter", "value"),
    [Input({"type": "keyword-button", "index": ALL}, "n_clicks")],
    [State({"type": "keyword-button", "index": ALL}, "id")],
    prevent_initial_call=True,
)
def update_keyword_selection(n_clicks, id):
    if any([n_click > 0 for n_click in n_clicks]):
        button_clicked = ctx.triggered_id
        if button_clicked:
            print(f"Keyword button was clicked: {button_clicked}")
            keyword = button_clicked["index"]
            return keyword
    else:
        return no_update


@app.callback(
    Output({"type": "publication-elem-button", "index": MATCH}, "children"),
    [Input({"type": "publication-elem-button", "index": MATCH}, "n_clicks")],
    [State({"type": "publication-elem-button", "index": MATCH}, "id")],
)
def update_publication_favorites(n_clicks, id):
    if n_clicks == 0:
        return no_update
    title = id["index"]
    favorites = client.get_favorites()
    favorited = title in favorites
    print((title, favorited, favorites))
    client.remove_favorite(title) if favorited else client.insert_favorite(title)

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
    Output("keyword-trend-chart", "figure"),
    Input("keyword-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_keyword_trend_chart(keyword, start_date, end_date):
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])
    df = client.get_keyword_usage(
        keyword=keyword,
        start_year=start_year,
        end_year=end_year,
    )
    palette = cycle(px.colors.sequential.Blugrn)
    fig = go.Figure()
    fig.layout = {
        "title": {
            "text": "Keyword Trends",
            "x": 0.05,
            "xanchor": "left",
        },
        "xaxis": {"fixedrange": True},
        "yaxis": {"fixedrange": True},
    }
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["citations"],
            mode="lines+markers",
            name="Citations",
            marker_color=next(palette),
            hovertemplate="Citations: %{y:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["publications"],
            mode="lines+markers",
            name="Publications",
            marker_color=next(palette),
            hovertemplate="Publications: %{y:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["relevance"],
            mode="lines+markers",
            name="Relevant Citations",
            marker_color=next(palette),
            hovertemplate="Relevant Citations: %{y:.2f}<extra></extra>",
        )
    )
    fig.update_layout(hovermode="x unified")
    fig.update_layout(xaxis=dict(tickmode="linear", tick0=start_year, dtick=1))
    return fig


if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(debug=True, dev_tools_ui=False)
