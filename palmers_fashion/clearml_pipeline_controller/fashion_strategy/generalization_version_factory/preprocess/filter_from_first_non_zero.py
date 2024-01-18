def filter_from_first_non_zero(group):
    first_non_zero_index = group[group['stock_palmers'].ne(0)].index.min()
    return group.loc[first_non_zero_index:]