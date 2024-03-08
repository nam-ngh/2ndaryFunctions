import pandas as pd

def compute_2D(df_all, d1: str, d2: str, d3: str=None, method='sum'):
    '''
    Returns df where rows are d1 uniques, columns are d2 uniques, cells are d2-by-d1-count or d3 analysis (if provided)

    Args:
    - df_all: df with full data
    - d1: primary categorical column - to be x-axis of plot.
    - d2: secondary categorical column - to be separate lines or bars in group.
    - d3: optional tertiary category whose value will either be sum or taken mean of for each combination of the first 2 cats.
    - method: 'sum', 'mean' or 'nunique'. Only use where d3 != None. If only d1 and d2 are provided count of each d2 by d1 will be taken
    '''
    df = pd.DataFrame(index=df_all[d1].drop_duplicates().sort_values())

    # iterate over each d2 unique value:
    for cat in df_all.loc[~(df_all[d2].isna()), d2].unique():
        if d3 is None:
            vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1]).size()
        elif d3 is not None:
            if method=='sum':
                vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1])[d3].sum()
            elif method=='mean':
                vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1])[d3].mean()
            elif method=='nunique':
                vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1])[d3].nunique()
        
        # rename vals_by_d1 and merge into df
        vals_by_d1.name = cat
        df = pd.merge(df, vals_by_d1, how='left', left_index=True, right_index=True,)
    
    df = df.fillna(0)
    df['total'] = df.sum(axis=1)
    return df

def compute_2D_multiple_d2(df_all, d1: str, d2: list, d3: str=None, method='sum'):
    '''
    Returns df where rows are d1 uniques, columns are d2 uniques, cells are d2-by-d1-count or d3 analysis (if provided)

    Args:
    - df_all: df with full data
    - d1: primary categorical column - to be x-axis of plot.
    - d2: list of secondary categorical columns - to be separate lines or bars in group. Value type in each d2 col should be 0,1
    - d3: optional tertiary category whose value will either be sum or taken mean of for each combination of the first 2 cats.
    - method: 'sum' or 'mean'. When d3 is not None, also 'nunique'
    '''
    df = pd.DataFrame(index=df_all[d1].drop_duplicates().sort_values())

    # iterate over each d2 columns:
    for cat in d2:
        if d3 is None:
            if method=='sum':
                vals_by_d1 = df_all.groupby([d1])[cat].sum()
            elif method=='mean':
                vals_by_d1 = df_all.groupby([d1])[cat].mean()
        elif d3 is not None:
            if method=='sum':
                vals_by_d1 = df_all.loc[df_all[cat]==1].groupby([d1])[d3].sum()
            elif method=='mean':
                vals_by_d1 = df_all.loc[df_all[cat]==1].groupby([d1])[d3].mean()
            elif method=='nunique':
                vals_by_d1 = df_all.loc[df_all[cat]==1].groupby([d1])[d3].nunique()
        
        # rename vals_by_d1 and merge into df
        vals_by_d1.name = cat
        df = pd.merge(df, vals_by_d1, how='left', left_index=True, right_index=True,)
    
    df = df.fillna(0)
    df['total'] = df.sum(axis=1)
    return df