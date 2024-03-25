import plotly.graph_objects as go
import pandas

def plot_2D(df_2D, title: str='', plot_total: bool=False, 
    columns: list=None, bar: bool=False, bar_mode: str='group', 
    line_fill: str='none',):
    
    '''
    Default multi-line plot for multiple categories. x = df index, y = df columns 

    Required: 2D df
    Optional: everything else

    Args:
    - df_2D: (pandas.DataFrame) containing data to be plotted. Index is mapped to x-axis, columns represent categories.
    - plot_total: (bool, optional) plots a total line or not. requires a total column in df_2d
    - columns: (list of str, optional) specify which columns in the df are plotted. Default=None plots all columns
    - bar: (bool, optional) plots categories as bars instead of lines
    - barmode: (str, optional with bar) 'group' or 'stack' bars
    - linefill: (str, optional) 'none', 'tozeroy' or 'tonexty'
    '''

    fig = go.Figure()
    if columns is None:
        cats = list(df_2D.columns) 
        if 'total' in df_2D.columns:
            total = df_2D['total']
            cats.remove('total')

    elif columns is not None:
        cats = columns
        total = df_2D[columns].sum(axis=1)

    for col in cats:
        if bar == False:
            fig.add_trace(go.Scatter(
                x=df_2D.index, y=df_2D[col], name=col,
                mode='lines+markers', marker=dict(line=dict(width=1)),
                fill=line_fill
            ))
        elif bar == True:
            fig.add_trace(go.Bar(x=df_2D.index, y=df_2D[col], name=col,))
    
    if plot_total == True:
        fig.add_trace(go.Scatter(
            x=total.index, y=total, name='Total',
            mode='lines+text', marker=dict(color='navy'), line=dict(width=5),
            text=df_2D['total'], textposition='top center'
        ))

    fig.update_layout(
        title=title,
        height=800,
        plot_bgcolor='white',
        yaxis=dict(
            gridcolor='lightgray'
        ),
        xaxis=dict(
            gridcolor='lightgray',
            showline=True, linecolor='black',
        ),
        barmode=bar_mode
    )
    return fig

def default_y2(range, title='',
    side='right', show_ticks=False,
    show_grid=False, grid_color='gray',
    show_line=False, line_color='black'):
    return {
        'title': title, 'side': side,
        'anchor':"x", 'overlaying':"y",
        'showticklabels': show_ticks, 'range': range,
        'showgrid': show_grid, 'gridcolor': grid_color, 
        'showline': show_line, 'linecolor': line_color
    }

def map_object_colour(all_objs: list, col_dict: dict, default_col: str='lightgray',):
    '''
    Returns {obj: col} map for every object in all_objects
    
    ARGS:
    - all_objs: list of all objects
    - col_dict: dict mapping special colours to lists of some special objects {col1: [obj1, obj2, etc.], ...}
    - default_col: colour to be applied to all objs not specified in col_dict
    '''
    obj_dict = {}
    for o in all_objs:
        obj_dict[o] = default_col
        for col in col_dict.keys():
            if o in col_dict[col]:
                obj_dict[o] = col
    
    return obj_dict