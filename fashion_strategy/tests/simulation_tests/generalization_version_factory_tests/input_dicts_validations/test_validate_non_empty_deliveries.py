import pytest
from   fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_non_empty_deliveries

# Test case 1: Both dict_deliveries_from_warehouse and dict_arrivals_store_deliveries are empty
dict_deliveries_from_warehouse_empty = {}
dict_arrivals_store_deliveries_empty = {}
@pytest.mark.parametrize("dict_deliveries_from_warehouse, dict_arrivals_store_deliveries, expected_result", [
    (dict_deliveries_from_warehouse_empty, dict_arrivals_store_deliveries_empty, False),
])

def test_validate_non_empty_deliveries_empty(dict_deliveries_from_warehouse, dict_arrivals_store_deliveries, expected_result):
    result = validate_non_empty_deliveries(dict_deliveries_from_warehouse, dict_arrivals_store_deliveries)
    assert result == expected_result

# Test case 2: dict_deliveries_from_warehouse is empty, but dict_arrivals_store_deliveries is not empty
dict_deliveries_from_warehouse_empty = {}
dict_arrivals_store_deliveries_valid = {
    '2022-01-01': ['Store1', 'Store2'],
    '2022-01-02': ['Store3'],
    '2022-01-03': [],
}
@pytest.mark.parametrize("dict_deliveries_from_warehouse, dict_arrivals_store_deliveries, expected_result", [
    (dict_deliveries_from_warehouse_empty, dict_arrivals_store_deliveries_valid, False),
])

def test_validate_non_empty_deliveries_warehouse_empty(dict_deliveries_from_warehouse, dict_arrivals_store_deliveries, expected_result):
    result = validate_non_empty_deliveries(dict_deliveries_from_warehouse, dict_arrivals_store_deliveries)
    assert result == expected_result

# Test case 3: dict_arrivals_store_deliveries is empty, but dict_deliveries_from_warehouse is not empty
dict_deliveries_from_warehouse_valid = {
    '2022-01-01': ['Store1', 'Store2'],
    '2022-01-02': ['Store3'],
    '2022-01-03': [],
}
dict_arrivals_store_deliveries_empty = {}
@pytest.mark.parametrize("dict_deliveries_from_warehouse, dict_arrivals_store_deliveries, expected_result", [
    (dict_deliveries_from_warehouse_valid, dict_arrivals_store_deliveries_empty, False),
])

def test_validate_non_empty_deliveries_arrivals_empty(dict_deliveries_from_warehouse, dict_arrivals_store_deliveries, expected_result):
    result = validate_non_empty_deliveries(dict_deliveries_from_warehouse, dict_arrivals_store_deliveries)
    assert result == expected_result

# Test case 4: Both dict_deliveries_from_warehouse and dict_arrivals_store_deliveries are not empty
dict_deliveries_from_warehouse_valid = {
    '2022-01-01': ['Store1', 'Store2'],
    '2022-01-02': ['Store3'],
    '2022-01-03': [],
}
dict_arrivals_store_deliveries_valid = {
    '2022-01-01': ['Store1', 'Store2'],
    '2022-01-02': ['Store3'],
    '2022-01-03': [],
}
@pytest.mark.parametrize("dict_deliveries_from_warehouse, dict_arrivals_store_deliveries, expected_result", [
    (dict_deliveries_from_warehouse_valid, dict_arrivals_store_deliveries_valid, True),
])

def test_validate_non_empty_deliveries_valid(dict_deliveries_from_warehouse, dict_arrivals_store_deliveries, expected_result):
    result = validate_non_empty_deliveries(dict_deliveries_from_warehouse, dict_arrivals_store_deliveries)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()
