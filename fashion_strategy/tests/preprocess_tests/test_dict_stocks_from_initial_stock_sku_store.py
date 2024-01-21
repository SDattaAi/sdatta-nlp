import pytest
import pandas as pd
from fashion_strategy.simulation.generalization_version_factory.preprocess import dict_stocks_from_initial_stock_sku_store


initial_stock_sku_store1 = pd.DataFrame({
    'store': ['VZ01', 'VZ01', 'VZ01', 'store1', 'store1', 'store1'],
    'sku': ['SKU1', 'SKU2', 'SKU3', 'SKU1', 'SKU2', 'SKU3'],
    'initial_stock': [100, 200, 50, 100, 50, 75],
    'first_initial_stock_date': ['2022-01-01', '2022-01-01', '2022-01-01', '2022-01-02', '2022-01-02', '2022-01-01']
})
relevant_stores1 = ['VZ01', 'store1']
expected_output1 = {'VZ01': {'SKU1': 0, 'SKU2': 150, 'SKU3': 50},
 'store1': {'SKU1': 100, 'SKU2': 50, 'SKU3': 75}}


@pytest.mark.parametrize("initial_stock_sku_store, relevant_stores, expected_output", [
    (initial_stock_sku_store1, relevant_stores1, expected_output1),
])
def test_dict_stocks_from_initial_stock_sku_store(initial_stock_sku_store, relevant_stores, expected_output):
    result = dict_stocks_from_initial_stock_sku_store(initial_stock_sku_store, relevant_stores)
    assert result == expected_output

