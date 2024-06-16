from itertools import product
import plotly.graph_objects as go
import plotly.express as px


def get_table_fig(ent, first_n=20, width=600, height=800, **kwargs):
    df = ent['frame']
    if isinstance(df.columns[0], tuple):
        col_index_size = len(df.columns[0])
    else:
        col_index_size = 1
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=df.columns.tolist()),
                cells=dict(
                    values=df.iloc[col_index_size:first_n].values.T.tolist()),
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


def get_plot_fig(ent, x_col, y_cols, sort_by_x=True, first_n=20, width=600, height=800, is_plotly_obj=True, **kwargs):
    df = ent['frame']
    title = ent['meta']
    if isinstance(title, dict):
        title = title.get('title', '')
    if isinstance(df.columns[0], tuple):
        col_index_size = len(df.columns[0])
    else:
        col_index_size = 1

    if sort_by_x:
        df = df.sort_values(by=x_col)

    if first_n:
        df = df.iloc[col_index_size:first_n]

    x = df[x_col].values.tolist()
    y = [df[y_col].values.tolist() for y_col in y_cols]
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x,
                y=df[y_col].values.tolist(),
                name=str(y_col)
            )
            for y_col in y_cols
        ],
    )
    if not is_plotly_obj:
        return {'x': x, 'y': y, 'title': title, 'type': 'line'}

    fig.update_layout(
        title=title,
        # width=width, height=height,
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
    x_col = None
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
    y_cols = []
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


def get_pie_chart_settings(entity):
    cat_cols = None
    float_cols = None
    pie_chart_settings = []
    if 'category' not in entity['col_types']:
        return []
    if 'category' in entity['col_types']:
        cat_cols = entity['col_types']['category']
        if 'float' in entity['col_types']:
            float_cols = entity['col_types']['float']

    if cat_cols and float_cols:
        for cat, flot in product(cat_cols, float_cols):
            setting = {
                'type': 'pie',
                'cat_col': cat,
                'float_col': flot,
            }
            pie_chart_settings.append(setting)
    elif cat_cols:
        for cat in cat_cols:
            setting = {
                'type': 'pie',
                'cat_col': cat
            }
            pie_chart_settings.append(setting)
    return pie_chart_settings


def get_line_chart_settings(entity):
    x_cols = None
    y_cols = None

    if 'datetime' in entity['col_types']:
        x_cols = entity['col_types']['datetime']
        if 'float' in entity['col_types']:
            # если есть зависимость от времени - рисуем ее
            y_cols = entity['col_types']['float']
            line_chart_settings = []
            for x_col in x_cols:
                setting = {
                    'type': 'line',
                    'x_col': x_col,
                    'y_cols': y_cols
                }
                line_chart_settings.append(setting)
            return line_chart_settings

    elif 'float' in entity['col_types']:
        if len(entity['col_types']) < 2:
            return []
        line_chart_settings = []
        for i, x_col in enumerate(entity['col_types']['float']):
            # берем в y_cols все кроме i-того столбца
            y_cols = entity['col_types']['float'][:i]
            if i + 1 != len(entity['col_types']['float']):
                y_cols += entity['col_types']['float'][i + 1:]
            setting = {
                'type': 'line',
                'x_col': x_col,
                'y_cols': y_cols,
            }
            line_chart_settings.append(setting)
        return line_chart_settings

    # если нет дейттайма и флотов, то не можем построить линию
    return []


def get_pie_chart(entity, cat_col=None, float_col=None, is_plotly_obj=True, **kwargs):
    title = entity['meta']
    if isinstance(title, dict):
        title = title.get('title', '')
    if cat_col is None:
        return None
    if isinstance(cat_col, tuple):
        cat_col = list(cat_col)

    if float_col is None:
        try:
            groupped = entity['frame'].groupby(cat_col)[cat_col].count()
        except ValueError:
            return None  # Какая-то ерунда с многоуровневыми индексами, починить если хватит времени
        values = groupped.values.tolist()
        names = groupped.index.tolist()
    else:
        values = entity['frame'][float_col].values.tolist()
        names = entity['frame'][cat_col].values.tolist()
    fig = go.Figure(data=[go.Pie(labels=names, values=values, title=title)])
    if not is_plotly_obj:
        return {'values': values, 'names': names, 'title': title, 'type': 'pie'}
    return fig


def get_all_possible_charts(entity):
    charts = []
    line_chart_settings = get_line_chart_settings(entity)
    charts += [get_plot_fig(entity, **settings)
               for settings in line_chart_settings][:1]  # выбирать по умному
    pie_chart_settings = get_pie_chart_settings(entity)
    print(pie_chart_settings)
    charts += [get_pie_chart(entity, **settings)
               for settings in pie_chart_settings][:1]  # выбирать по умному
    charts += [get_table_fig(entity)]
    return charts


def get_one_figure_by_entity(entity, return_plotly_format=False):
    # print(type(entity['frame']))
    line_chart_settings = get_line_chart_settings(entity)
    line_charts = [get_plot_fig(entity, is_plotly_obj=return_plotly_format, **settings)
                   for settings in line_chart_settings]
    # print('line charts', len(line_charts))
    
    pie_chart_settings = get_pie_chart_settings(entity)
    pie_charts = [get_pie_chart(entity, is_plotly_obj=return_plotly_format, **settings)
                  for settings in pie_chart_settings]
    # print('pie charts', len(pie_charts))
    if pie_charts:
        return pie_charts[0]
    if line_charts:
        return line_charts[0]
    return None
    # return get_table_fig(entity)
