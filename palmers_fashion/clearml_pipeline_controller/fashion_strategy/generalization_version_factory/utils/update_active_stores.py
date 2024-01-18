def update_active_stores(ActiveStores: dict, dict_stocks: dict) -> dict:
    """
    This function update ActiveStores (note: update by hard data from the past from outside the simulation)


    assumption for now: all the stores are active
    for later: we will need to decide which stores are active and which are not by timeline interval rule
    Args:
    --------
    ActiveStores: dict
        ActiveStores[store] = 1/0
    dict_stocks: dict
        dict_stocks[store][sku] = amount
    -------
    return: ActiveStores
    """
    return ActiveStores