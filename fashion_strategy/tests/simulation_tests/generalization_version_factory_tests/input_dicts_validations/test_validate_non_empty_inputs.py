import pytest
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_non_empty_inputs

# Test case 1: Both dict_stocks and dict_sales are empty
dict_stocks_empty = {}
dict_sales_empty = {}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_empty, dict_sales_empty, False),
])

def test_validate_non_empty_inputs_empty(dict_stocks, dict_sales, expected_result):
    result = validate_non_empty_inputs(dict_stocks, dict_sales)
    assert result == expected_result

# Test case 2: dict_stocks is empty, but dict_sales is not empty
dict_stocks_empty = {}
dict_sales_valid = {
    'Store1': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Store2': ['2022-01-01', '2022-01-02', '2022-01-03'],
}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_empty, dict_sales_valid, False),
])

def test_validate_non_empty_inputs_dict_stocks_empty(dict_stocks, dict_sales, expected_result):
    result = validate_non_empty_inputs(dict_stocks, dict_sales)
    assert result == expected_result

# Test case 3: dict_stocks is not empty, but dict_sales is empty
dict_stocks_valid = {
    'Store1': {'SKU1': 100, 'SKU2': 200},
    'Store2': {'SKU1': 50, 'SKU3': 150},
}
dict_sales_empty = {}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_valid, dict_sales_empty, False),
])

def test_validate_non_empty_inputs_dict_sales_empty(dict_stocks, dict_sales, expected_result):
    result = validate_non_empty_inputs(dict_stocks, dict_sales)
    assert result == expected_result

# Test case 4: Both dict_stocks and dict_sales are not empty
dict_stocks_valid = {
    'Store1': {'SKU1': 100, 'SKU2': 200},
    'Store2': {'SKU1': 50, 'SKU3': 150},
}
dict_sales_valid = {
    'Store1': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Store2': ['2022-01-01', '2022-01-02', '2022-01-03'],
}
@pytest.mark.parametrize("dict_stocks, dict_sales, expected_result", [
    (dict_stocks_valid, dict_sales_valid, True),
])

def test_validate_non_empty_inputs_valid(dict_stocks, dict_sales, expected_result):
    result = validate_non_empty_inputs(dict_stocks, dict_sales)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()
