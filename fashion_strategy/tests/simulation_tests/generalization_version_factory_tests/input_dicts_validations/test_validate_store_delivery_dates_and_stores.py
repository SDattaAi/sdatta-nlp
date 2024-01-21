import pytest
from datetime import datetime
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_store_delivery_dates_and_stores

# Test case 1: All delivery dates have valid format
dict_deliveries_valid_dates = {
    '2022-01-01': ['Store1', 'Store2'],
    '2022-01-02': ['Store3'],
    '2022-01-03': [],
}
@pytest.mark.parametrize("dict_deliveries, expected_result", [
    (dict_deliveries_valid_dates, True),
])

def test_validate_store_delivery_dates_and_stores_valid_dates(dict_deliveries, expected_result):
    result = validate_store_delivery_dates_and_stores(dict_deliveries)
    assert result == expected_result

# Test case 2: Some delivery dates have invalid format
dict_deliveries_invalid_dates = {
    '2022-01-01': ['Store1', 'Store2'],
    '2022-01-02': ['Store3'],
    '2022-13-01': [],  # Invalid date format
}
@pytest.mark.parametrize("dict_deliveries, expected_result", [
    (dict_deliveries_invalid_dates, False),
])

def test_validate_store_delivery_dates_and_stores_invalid_dates(dict_deliveries, expected_result):
    result = validate_store_delivery_dates_and_stores(dict_deliveries)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()
