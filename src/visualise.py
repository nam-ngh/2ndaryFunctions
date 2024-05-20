import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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

def plot_4by4(df: pd.DataFrame, plot_type: str='kde', col_group: int=0):
    '''
    Plots distribution for all columns of a df.
    Args:
    - df: input (pd.DataFrame)
    - plot_type: (string) 'kde' or 'box'
    - col_group: if df has more than 16 columns, use col_group to specify the group to be plotted (0,1,2,...)
    '''
    fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(24,24))
    cols = df.columns[(16*col_group):(16*(col_group + 1))]
    for i, column in enumerate(cols):
        if plot_type == 'kde':
            sns.kdeplot(df[column],ax=axes[i//4,i%4], color='orange')
        elif plot_type == 'box':
            sns.boxplot(df[column],ax=axes[i//4,i%4])
        axes[i//4,i%4].set_title(column)
        # Hide top and right spines
        axes[i//4,i%4].spines['top'].set_visible(False)
        axes[i//4,i%4].spines['right'].set_visible(False)
    return fig