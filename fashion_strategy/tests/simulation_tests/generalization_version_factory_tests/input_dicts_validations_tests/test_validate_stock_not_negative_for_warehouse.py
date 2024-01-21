import pytest
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_stock_not_negative_for_warehouse

# Test case 1: All stocks for the warehouse are non-negative
dict_stocks_non_negative = {
    'VZ01': {'SKU1': 100, 'SKU2': 200},
    'Store1': {'SKU1': 50, 'SKU3': 150},
}
warehouse_store_valid = 'VZ01'
@pytest.mark.parametrize("dict_stocks, warehouse_store, expected_result, expected_list_to_delete", [
    (dict_stocks_non_negative, warehouse_store_valid, (True, []), []),
])

def test_validate_stock_not_negative_for_warehouse_valid(dict_stocks, warehouse_store, expected_result, expected_list_to_delete):
    result = validate_stock_not_negative_for_warehouse(dict_stocks, warehouse_store)
    assert result == expected_result

# Test case 2: Some stocks for the warehouse are negative
dict_stocks_negative = {
    'VZ01': {'SKU1': 100, 'SKU2': -20},
    'Store1': {'SKU1': 50, 'SKU3': 150},
}
warehouse_store_invalid = 'VZ01'
expected_list_to_delete_invalid = ['SKU2']
@pytest.mark.parametrize("dict_stocks, warehouse_store, expected_result, expected_list_to_delete", [
    (dict_stocks_negative, warehouse_store_invalid, (False, expected_list_to_delete_invalid), expected_list_to_delete_invalid),
])

def test_validate_stock_not_negative_for_warehouse_invalid(dict_stocks, warehouse_store, expected_result, expected_list_to_delete):
    result = validate_stock_not_negative_for_warehouse(dict_stocks, warehouse_store)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()
