import pytest
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_positive_stocks

# Test case 1: All stocks for all stores are non-negative
dict_stocks_non_negative = {
    'VZ01': {'SKU1': 100, 'SKU2': 200},
    'Store1': {'SKU1': 50, 'SKU3': 150},
}
@pytest.mark.parametrize("dict_stocks, expected_result, expected_negative_warehouse_stocks", [
    (dict_stocks_non_negative, True, []),
])

def test_validate_positive_stocks_valid(dict_stocks, expected_result, expected_negative_warehouse_stocks):
    result = validate_positive_stocks(dict_stocks)
    assert result == expected_result

# Test case 2: Some stocks for some stores are negative
dict_stocks_negative = {
    'VZ01': {'SKU1': 100, 'SKU2': -20},
    'Store1': {'SKU1': 50, 'SKU3': 150},
}
expected_negative_warehouse_stocks_invalid = ['VZ01']
@pytest.mark.parametrize("dict_stocks, expected_result, expected_negative_warehouse_stocks", [
    (dict_stocks_negative, False, expected_negative_warehouse_stocks_invalid),
])

def test_validate_positive_stocks_invalid(dict_stocks, expected_result, expected_negative_warehouse_stocks):
    result = validate_positive_stocks(dict_stocks)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()
