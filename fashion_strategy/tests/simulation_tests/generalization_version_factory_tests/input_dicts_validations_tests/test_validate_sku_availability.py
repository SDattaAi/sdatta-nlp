import pytest
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_sku_availability

# Test case 1: All SKUs in sales data are available in at least one store
dict_stocks_valid = {
    'Store1': {'SKU1': 100, 'SKU2': 200},
    'Store2': {'SKU1': 50, 'SKU3': 150},
}
dict_sales_valid_sku = {
    'Store1': {
        '2022-01-01': [('SKU1', 10), ('SKU2', 20)],
        '2022-01-02': [('SKU1', 5)],
    },
    'Store2': {
        '2022-01-01': [('SKU1', 25)],
    },
}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_valid, dict_sales_valid_sku, True),
])

def test_validate_sku_availability_valid_sku(dict_stocks, dict_sales, expected_result):
    result = validate_sku_availability(dict_stocks, dict_sales)
    assert result == expected_result

# Test case 2: Some SKUs in sales data are not available in any store
dict_stocks_invalid_sku = {
    'Store1': {'SKU1': 100, 'SKU2': 200},
    'Store2': {'SKU1': 50, 'SKU3': 150},
}
dict_sales_invalid_sku = {
    'Store1': {
        '2022-01-01': [('SKU1', 10), ('SKU2', 20)],
        '2022-01-02': [('SKU1', 5), ('SKU4', 30)],  # SKU4 is not in any store
    },
    'Store2': {
        '2022-01-01': [('SKU1', 25)],
    },
}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_invalid_sku, dict_sales_invalid_sku, False),
])

def test_validate_sku_availability_invalid_sku(dict_stocks, dict_sales, expected_result):
    result = validate_sku_availability(dict_stocks, dict_sales)
    assert result == expected_result

# Test case 3: All SKUs are missing from sales data
dict_stocks_missing_sku = {
    'Store1': {'SKU1': 100, 'SKU2': 200},
    'Store2': {'SKU1': 50, 'SKU3': 150},
}
dict_sales_missing_sku = {
    'Store1': {
        '2022-01-01': [],
        '2022-01-02': [],
    },
    'Store2': {
        '2022-01-01': [],
    },
}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_missing_sku, dict_sales_missing_sku, True),
])

def test_validate_sku_availability_missing_sku(dict_stocks, dict_sales, expected_result):
    result = validate_sku_availability(dict_stocks, dict_sales)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()
