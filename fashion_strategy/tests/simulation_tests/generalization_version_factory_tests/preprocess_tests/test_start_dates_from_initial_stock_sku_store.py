import pytest
import pandas as pd
from fashion_strategy.simulation.generalization_version_factory.preprocess import start_dates_from_initial_stock_sku_store

initial_stock_sku_store1 = pd.DataFrame({
    'store': ['VZ01', 'VZ01', 'store1', 'store1'],
    'sku': ['SKU1', 'SKU2', 'SKU1', 'SKU2'],
    'initial_stock': [100, 0, 100, 50],
    'first_initial_stock_date': ['2022-01-01', '2022-01-01', '2022-01-02', '2022-01-01']
})

relevant_stores1 = ['VZ01', 'store1']

expected_output1 = {
    '2022-01-01': [('SKU1', 'VZ01'), ('SKU2', 'store1')],
    '2022-01-02': [('SKU1', 'store1')],
}

@pytest.mark.parametrize("initial_stock_sku_store, relevant_stores, expected_output", [
    (initial_stock_sku_store1, relevant_stores1, expected_output1),
])
def test_start_dates_from_initial_stock_sku_store(initial_stock_sku_store, relevant_stores, expected_output):
    result = start_dates_from_initial_stock_sku_store(initial_stock_sku_store, relevant_stores)
    assert result == expected_output

