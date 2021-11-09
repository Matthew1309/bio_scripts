# Purpose of this file is to put nice little pandas functions I have developed
# into an importable module.

###===

import pandas as pd

def categorical_exploration(df, column_to_group_by, column_to_summarize):
    '''
    Usage: categorical_exploration(df, 'column1', 'column2')

    Returns a pandas df with counts of category-column2 in
            category-column1.
    '''

    # Get unique set of "group by" categories from the first input
    categories_to_group_by = set(df[column_to_group_by])
    # For each "group by" category, get its unique set of values in another column
    categorical_exploration_dict = {groupby: df[ df[column_to_group_by] == groupby ][column_to_summarize].value_counts().to_dict() for groupby in categories_to_group_by}     
    # Return a pandas dataframe with the group-by columns as the
    # observation (along index) and the summarize columns as the 
    # column headers. Fill unknowns with NaNs.
    return( pd.DataFrame.from_dict(categorical_exploration_dict, orient='index'))

###===
