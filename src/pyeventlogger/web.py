import webbrowser
from multiprocessing import Process

import dash
import pandas as pd
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)


def build_layout(df: pd.DataFrame):
    app.layout = dash_table.DataTable(
        id="datatable-interactivity",
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict("records"),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="none",
        style_table={"overflowY": "auto"},
        css=[{"selector": "table", "rule": "table-layout: fixed"}],
        style_cell={
            "width": "{}%".format(len(df.columns)),
            "textOverflow": "ellipsis",
            "overflow": "hidden",
        },
    )
    return app


@app.callback(
    Output("datatable-interactivity", "style_data_conditional"),
    Input("datatable-interactivity", "selected_columns"),
)
def update_styles(selected_columns):
    return [
        {"if": {"column_id": i}, "background_color": "#D2F3FF"}
        for i in selected_columns
    ]


def launch_browser(ip: str, port: str):
    webbrowser.open(f"http://{ip}:{port}/")


def launch_server(ip: str, port: str, df: pd.DataFrame):
    app = build_layout(df)
    app.run_server(port=port, host=ip)


def start_server(df: pd.DataFrame):
    port = "8050"
    ip = "127.0.0.1"

    browser = Process(target=launch_browser, args=(ip, port))
    server = Process(target=launch_server, args=(ip, port, df))

    server.start()
    browser.start()

    server.join()
    browser.join()
