import pandas as pd
import database as db
from itertools import cycle
import plotly.express as px
import plotly.graph_objects as go
from requests.utils import requote_uri
from dash import Dash, Input, Output, State, dcc, html, MATCH, ALL

# from dash import dash_table

gds = db.gds.Client(database="academicworld")
mysql = db.mysql.Client(database="academicworld")
mongo = db.mongo.Client(database="academicworld")
neo4j = db.neo4j.Client(database="academicworld")
prepared = db.prepared.Client(database="academicworld")


keywords = [keyword["name"] for keyword in mysql.execute(query=mysql.get_keywords)]


def get_similar_keywords(**kwargs):
    gds.project_if_not_exists(
        "keyword-label-pub",
        {
            "nodes": ["PUBLICATION", "KEYWORD"],
            "relationships": {
                "LABEL_BY": {"properties": "score", "orientation": "REVERSE"}
            },
        },
    )
    return [
        match["keyword2"]
        for match in neo4j.execute(query=neo4j.get_similar_keywords, **kwargs)
    ]


def get_most_relevant_publications(**kwargs):
    return [
        publication["title"]
        for publication in mysql.execute(
            query=mysql.get_most_relevant_publications, **kwargs
        )
    ]
 
def get_faculty_top_score(**kwargs):
    return [
        faculty["faculty_name"]
        for faculty in mysql.execute(
            query=mysql.get_faculty_top_scores, **kwargs
        )
    ]  

def get_faculty_relationship(**kwargs):
    return [
        faculty["keyword"]
        for faculty in neo4j.execute(
            query=neo4j.get_faculty_relations, **kwargs
        )
    ]

def get_most_relevant_university(**kwargs):
    return [
        institute["institute"]
        for institute in neo4j.execute(
            query=neo4j.get_most_relevant_universities, **kwargs
        )
    ]


def get_most_relevant_university_publications(**kwargs):
    return [
        publication["title"]
        for publication in neo4j.execute(
            query=neo4j.get_university_publications, **kwargs
        )
    ]


def get_most_relevant_faculty(**kwargs):
    return [
        faculty["faculty"]
        for faculty in neo4j.execute(query=neo4j.get_most_relevant_faculty, **kwargs)
    ]


def get_most_relevant_faculty_publications(**kwargs):
    return [
        publication["title"]
        for publication in neo4j.execute(query=neo4j.get_faculty_publications, **kwargs)
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
                html.A(
                    publication,
                    href=requote_uri(
                        f'https://scholar.google.com/scholar?hl=en&q="{publication}"'
                    ),
                    target="_blank",
                ),
                # publication,
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
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    # suppress_callback_exceptions=True,
)
app.title = "Keyword Explorer"
# https://stackoverflow.com/questions/59568510/dash-suppress-callback-exceptions-not-working
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Keyword Explorer", className="header-title"),
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
                        html.Div(children="Keywords", className="menu-title"),
                        dcc.Dropdown(
                            id="keyword-filter",
                            options=[
                                {"label": keyword, "value": keyword}
                                for keyword in keywords
                            ],
                            # value="internet",
                            value="abnormality detection",
                            # placeholder="Select a keyword",
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
                        label="Research Interest",
                        value="faculty-score",
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
    ]
)


@app.callback(
    Output("similar-keywords", "children"),
    Input("keyword-filter", "value"),
)
def update_similar_keywords(keyword):
    keywords = get_similar_keywords(keyword=keyword)
    return html.Div(children=", ".join(keywords), className="recommendations")


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
    elif tab == "top-universities":
        top_universities = get_most_relevant_university(
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
                    # value="Stanford University",
                    placeholder="Select a university from the rankings",
                    clearable=False,
                    className="dropdown",
                    style={
                        "min-width": "1024px",
                        "height": "54px",
                        "font-weight": "500",
                    },
                ),
                html.Div(children=[], id="university-publications"),
            ]
        )
    elif tab == "top-researchers":
        top_researchers = get_most_relevant_faculty(
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
                    # value="Alan Ford",
                    placeholder="Select a researcher from the rankings",
                    clearable=False,
                    className="dropdown",
                    style={
                        "min-width": "1024px",
                        "height": "54px",
                        "font-weight": "500",
                    },
                ),
                html.Div(children=[], id="researcher-publications"),
            ]
        )
    elif tab == "faculty-score":
        faculties = get_faculty_top_score()
        faculties = list(dict.fromkeys(faculties)) # remove duplicates
        return html.Div(
            children=[
                dcc.Dropdown(
                    id="faculty-filter",
                    options=[
                        {"label": faculty, "value": faculty}
                        for faculty in faculties
                    ],
                    # value="Alan Ford",
                    placeholder="Select a Faculty",
                    clearable=False,
                    className="dropdown",
                    style={
                        "min-width": "1024px",
                        "height": "54px",
                        "font-weight": "500",
                    },
                ),
                html.Div(children=[], id="faculty-relations"),
            ]
        )
    elif tab == "favorites":
        favorites = get_favorites()
        return html.Div(children=generate_publication_list(favorites))

@app.callback(
    Output("faculty-relations", "children"),
    Input("faculty-filter", "value"),
    # prevent_initial_call=True,
)
def update_faculty_relations(faculty):
    return html.Div(children=[html.Li(r) for r in get_faculty_relationship(faculty=faculty)])
        

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
    return html.Div(
        children=generate_publication_list(
            get_most_relevant_university_publications(
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
    # prevent_initial_call=True,
)
def update_researcher_publications(researcher, keyword, start_date, end_date):
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])
    return html.Div(
        children=generate_publication_list(
            get_most_relevant_faculty_publications(
                faculty=researcher,
                keyword=keyword,
                start_year=start_year,
                end_year=end_year,
            )
        )
    )


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
    df = pd.DataFrame(
        mongo.execute(
            query=mongo.get_keywords_trends,
            keyword=keyword,
            start_year=start_year,
            end_year=end_year,
        )
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
    app.run_server(debug=True, dev_tools_ui=False)
