import pytest
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_store_sku_identifiers

# Test case 1: Both dict_stocks and dict_sales are empty
dict_stocks_empty = {}
dict_sales_empty = {}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_empty, dict_sales_empty, True),
])
def test_validate_store_sku_identifiers_empty(dict_stocks, dict_sales, expected_result):
    result = validate_store_sku_identifiers(dict_stocks, dict_sales)
    assert result == expected_result

# Test case 2: All stores and SKUs in dict_sales are valid
dict_stocks_valid = {
    'Store1': {'SKU1': 100, 'SKU2': 200},
    'Store2': {'SKU1': 50, 'SKU3': 150},
}
dict_sales_valid = {
    'Store1': {
        '2022-01-01': [('SKU1', 10), ('SKU2', 20)],
        '2022-01-02': [('SKU1', 5)],
    },
    'Store2': {
        '2022-01-01': [('SKU1', 25)],
    },
}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_valid, dict_sales_valid, True),
])

def test_validate_store_sku_identifiers_valid(dict_stocks, dict_sales, expected_result):
    result = validate_store_sku_identifiers(dict_stocks, dict_sales)
    assert result == expected_result

# Test case 3: Some stores in dict_sales are not valid
dict_stocks_invalid_store = {
    'Store1': {'SKU1': 100, 'SKU2': 200},
    'Store2': {'SKU1': 50, 'SKU3': 150},
}
dict_sales_invalid_store = {
    'Store1': {
        '2022-01-01': [('SKU1', 10), ('SKU2', 20)],
        '2022-01-02': [('SKU1', 5)],
    },
    'Store3': {  # Store3 is not in dict_stocks
        '2022-01-01': [('SKU1', 25)],
    },
}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_invalid_store, dict_sales_invalid_store, False),
])

def test_validate_store_sku_identifiers_invalid_store(dict_stocks, dict_sales, expected_result):
    result = validate_store_sku_identifiers(dict_stocks, dict_sales)
    assert result == expected_result

# Test case 4: Some SKUs in dict_sales are not valid
dict_stocks_invalid_sku = {
    'Store1': {'SKU1': 100, 'SKU2': 200},
    'Store2': {'SKU1': 50, 'SKU3': 150},
}
dict_sales_invalid_sku = {
    'Store1': {
        '2022-01-01': [('SKU1', 10), ('SKU2', 20)],
        '2022-01-02': [('SKU1', 5), ('SKU4', 30)],  # SKU4 is not in dict_stocks
    },
    'Store2': {
        '2022-01-01': [('SKU1', 25)],
    },
}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_invalid_sku, dict_sales_invalid_sku, False),
])

def test_validate_store_sku_identifiers_invalid_sku(dict_stocks, dict_sales, expected_result):
    result = validate_store_sku_identifiers(dict_stocks, dict_sales)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()
