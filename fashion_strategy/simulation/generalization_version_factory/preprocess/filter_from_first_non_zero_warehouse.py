def filter_from_first_non_zero_warehouse(group):
    first_non_zero_index = group[group['warehouse_stock'].ne(0)].index.min()
    return group.loc[first_non_zero_index:]