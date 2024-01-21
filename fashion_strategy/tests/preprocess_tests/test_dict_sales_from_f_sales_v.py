import pytest
import pandas as pd
from fashion_strategy.simulation.generalization_version_factory.preprocess import dict_sales_from_f_sales_v


f_sales_v_fashion1 = pd.DataFrame({
    'store': ['Store A', 'Store A', 'Store B', 'Store B'],
    'date': ['2022-01-01', '2022-01-01', '2022-01-01', '2022-01-02'],
    'sku': ['SKU1', 'SKU2', 'SKU1', 'SKU2'],
    'sales': [100, 200, 150, 250]
})

expected_output1 = {
        'Store A': {
            '2022-01-01': [('SKU1', 100), ('SKU2', 200)],
        },
        'Store B': {
            '2022-01-01': [('SKU1', 150)],
            '2022-01-02': [('SKU2', 250)],
        },
    }

@pytest.mark.parametrize("f_sales_v_fashion, expected_output", [
    (f_sales_v_fashion1, expected_output1),
])
def test_dict_sales_from_f_sales_v(f_sales_v_fashion, expected_output):
    dict_sales = dict_sales_from_f_sales_v(f_sales_v_fashion)
    assert dict_sales == expected_output

