import pytest
from datetime import datetime
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_start_end_dates

# Test case 1: Both start_dates and end_dates are empty
start_dates_empty = {}
end_dates_empty = {}
@pytest.mark.parametrize("start_dates, end_dates, expected_result", [
    (start_dates_empty, end_dates_empty, True),
])
def test_validate_start_end_dates_empty(start_dates, end_dates, expected_result):
    result = validate_start_end_dates(start_dates, end_dates)
    assert result == expected_result

# Test case 2: All start dates are before the respective end dates
start_dates_valid = {
    '2022-01-01': [('SKU1', 'Store1')],
    '2022-01-02': [('SKU2', 'Store2')],
}
end_dates_valid = {
    '2022-01-03': ['SKU1'],
    '2022-01-04': ['SKU2'],
}
@pytest.mark.parametrize("start_dates, end_dates, expected_result", [
    (start_dates_valid, end_dates_valid, True),
])

def test_validate_start_end_dates_valid(start_dates, end_dates, expected_result):
    result = validate_start_end_dates(start_dates, end_dates)
    assert result == expected_result

# Test case 3: Some start dates are after the respective end dates
start_dates_invalid = {
    '2022-01-01': [('SKU1', 'Store1')],
    '2022-01-04': [('SKU2', 'Store2')],
}
end_dates_invalid = {
    '2022-01-03': ['SKU1'],
    '2022-01-02': ['SKU2'],
}
@pytest.mark.parametrize("start_dates, end_dates, expected_result", [
    (start_dates_invalid, end_dates_invalid, False),
])

def test_validate_start_end_dates_invalid(start_dates, end_dates, expected_result):
    result = validate_start_end_dates(start_dates, end_dates)
    assert result == expected_result

# Test case 4: Some SKUs in start_dates have no corresponding end dates
start_dates_no_end_dates = {
    '2022-01-01': [('SKU1', 'Store1')],
    '2022-01-02': [('SKU2', 'Store2')],
}
end_dates_no_end_dates = {
    '2022-01-03': ['SKU1'],
}
@pytest.mark.parametrize("start_dates, end_dates, expected_result", [
    (start_dates_no_end_dates, end_dates_no_end_dates, True),
])

def test_validate_start_end_dates_no_end_dates(start_dates, end_dates, expected_result):
    result = validate_start_end_dates(start_dates, end_dates)
    assert result == expected_result

# Test case 5: Some end dates in end_dates have no corresponding start dates
start_dates_no_start_dates = {
    '2022-01-9': [('SKU1', 'Store1')],
}
end_dates_no_start_dates = {
    '2022-01-02': ['SKU1'],
    '2022-01-01': ['SKU2'],
}
@pytest.mark.parametrize("start_dates, end_dates, expected_result", [
    (start_dates_no_start_dates, end_dates_no_start_dates, False),
])

def test_validate_start_end_dates_no_start_dates(start_dates, end_dates, expected_result):
    result = validate_start_end_dates(start_dates, end_dates)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()
