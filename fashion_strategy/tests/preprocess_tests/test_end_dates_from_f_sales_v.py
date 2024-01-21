import pytest
import pandas as pd
from fashion_strategy.simulation.generalization_version_factory.preprocess import end_dates_from_f_sales_v

# Sample data for testing

f_sales_v_fashion1 = pd.DataFrame({
    'sku': ['SKU1', 'SKU2', 'SKU1', 'SKU2'],
    'sales': [100, 0, 50, 200],
    'date': ['2022-01-01', '2022-01-02', '2022-01-02', '2022-01-03']
})
f_sales_v_fashion1['date'] = pd.to_datetime(f_sales_v_fashion1['date'])
expected_output1 = {'2022-01-02': ['SKU1'], '2022-01-03': ['SKU2']}

@pytest.mark.parametrize("f_sales_v_fashion, expected_output", [
    (f_sales_v_fashion1, expected_output1),
])
def test_end_dates_from_f_sales_v(f_sales_v_fashion, expected_output):
    result = end_dates_from_f_sales_v(f_sales_v_fashion)
    assert result == expected_output

