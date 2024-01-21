import pytest
from datetime import datetime
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_sales_date_format

# Test case 1: All sales dates have valid format
dict_sales_valid_dates = {
    'Store1': {
        '2022-01-01': [('SKU1', 10), ('SKU2', 20)],
        '2022-01-02': [('SKU1', 5)],
    },
    'Store2': {
        '2022-01-01': [('SKU1', 25)],
    },
}
@pytest.mark.parametrize("dict_sales, expected_result", [
    (dict_sales_valid_dates, True),
])

def test_validate_sales_date_format_valid_dates(dict_sales, expected_result):
    result = validate_sales_date_format(dict_sales)
    assert result == expected_result

# Test case 2: Some sales dates have invalid format
dict_sales_invalid_dates = {
    'Store1': {
        '2022-01-01': [('SKU1', 10), ('SKU2', 20)],
        '2022-01-02': [('SKU1', 5)],
        '2022-13-01': [('SKU3', 15)],  # Invalid date format
    },
    'Store2': {
        '2022-01-01': [('SKU1', 25)],
    },
}
@pytest.mark.parametrize("dict_sales, expected_result", [
    (dict_sales_invalid_dates, False),
])

def test_validate_sales_date_format_invalid_dates(dict_sales, expected_result):
    result = validate_sales_date_format(dict_sales)
    assert result == expected_result

# Test case 3: All sales dates are missing
dict_sales_missing_dates = {
    'Store1': {},
    'Store2': {},
}
@pytest.mark.parametrize("dict_sales, expected_result", [
    (dict_sales_missing_dates, True),
])

def test_validate_sales_date_format_missing_dates(dict_sales, expected_result):
    result = validate_sales_date_format(dict_sales)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()
