import plotly.graph_objects as go


def get_table_fig(ent, first_n=20, width=600, height=800):
    df = ent['frame']
    if isinstance(df.columns[0], tuple):
        col_index_size = len(df.columns[0])
    else:
        col_index_size = 1
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=df.columns),
                cells=dict(values=df.iloc[col_index_size:first_n].values.T),
            )
        ],
    )

    fig.update_layout(
        title=ent['meta'],
        width=width, height=height
        # xaxis_title="X Axis Title",
        # yaxis_title="Y Axis Title",
        # legend_title="Legend Title",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )
    return fig


def get_plot_fig(ent, x_col, y_cols, sort_by_x=True, first_n=20, width=600, height=800):
    df = ent['frame']
    if isinstance(df.columns[0], tuple):
        col_index_size = len(df.columns[0])
    else:
        col_index_size = 1

    if sort_by_x:
        df = df.sort_values(by=x_col)

    if first_n:
        df = df.iloc[col_index_size:first_n]

    fig = go.Figure(
        data=[
            go.Scatter(
                x=df[x_col].values,
                y=df[y_col].values,
                name=y_col
            )
            for y_col in y_cols
        ],
    )

    fig.update_layout(
        title=ent['meta'],
        width=width, height=height,
        xaxis_title=x_col,
        # yaxis_title=,
        showlegend=True,
        # legend_xanchor='right',
        # legend_yanchor='top',
        legend_valign='bottom',
        # legend_title="Legend Title",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )
    return fig


def plot_entity(entity):

    plot_config = {
        'width': 1000,
        'height': 600,
        'first_n': None,
    }
    plot_type, x_col, y_cols = get_plot_type(entity)
    if plot_type == 'line':
        res = get_plot_fig(entity, x_col=x_col, y_cols=y_cols, **plot_config)
    else:
        res = get_table_fig(entity, **plot_config)
    # res.to_dict()
    return res


def plotly_obj_to_json(plotly_obj):
    return plotly_obj.to_dict()


def get_plot_type(entity):
    unique_values = entity['col_unique_values']

    plot_type_x = None
    if 'datetime' in entity['col_types']:
        # time series
        x_col = entity['col_types']['datetime'][0]
        plot_type_x = 'line'
    elif 'str' in entity['col_types']:
        # table?
        x_col = entity['col_types']['str'][0]
        plot_type_x = 'table'
    else:
        # scatter?
        pass

    plot_type_y = None
    if 'float' in entity['col_types']:
        # series
        y_cols = entity['col_types']['float']
        plot_type_y = 'line'
    else:
        # table? scatter?
        plot_type_y = 'table'
        pass

    if len(entity['frame']) < 5:
        plot_type_y = 'table'
        plot_type_x = 'table'

    if plot_type_x == 'line' and plot_type_y == 'line':
        plot_type = 'line'
    else:
        plot_type = 'table'

    return plot_type, x_col, y_cols
