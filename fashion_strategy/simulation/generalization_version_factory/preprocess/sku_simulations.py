def sku_simulations(df_stock):
    skus_simulation = df_stock["sku"].unique().tolist()
    return skus_simulation