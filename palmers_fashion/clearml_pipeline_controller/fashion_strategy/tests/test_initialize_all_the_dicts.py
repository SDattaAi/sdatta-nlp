
from ... fashion_strategy.simulation.simulation_general import initialize_all_the_dicts

def test_initialize_all_the_dicts():
    skus_simulation = [101, 102]
    dict_stocks = {'store1': {101: 50, 102: 30}, 'store2': {101: 60, 102: 20}}
    results = initialize_all_the_dicts(skus_simulation, dict_stocks)
    assert len(results) == 7
    AshlonStock, MissedSales, ActiveStores, current_stock, \
    accumulated_stocks, accumulated_AshlonStock, accumulated_ActiveStores = results
    assert set(AshlonStock.keys()) == {'store1', 'store2'}
    assert set(MissedSales.keys()) == {'store1', 'store2'}
    assert set(current_stock.keys()) == {'store1', 'store2'}
    assert set(accumulated_stocks.keys()) == {'store1', 'store2'}
    assert isinstance(accumulated_AshlonStock, list)
    assert isinstance(accumulated_ActiveStores, list)


