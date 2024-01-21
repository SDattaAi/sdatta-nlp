import pytest
from datetime import datetime
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_sales_dates_within_simulation_period

# Test case 1: All sales dates are within the simulation period
dict_sales_valid_dates = {
    'Store1': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Store2': ['2022-01-01', '2022-01-02', '2022-01-03'],
}
start_date_valid = '2022-01-01'
end_date_valid = '2022-01-03'
@pytest.mark.parametrize("dict_sales, start_date, end_date, expected_result", [
    (dict_sales_valid_dates, start_date_valid, end_date_valid, True),
])

def test_validate_sales_dates_within_simulation_period_valid_dates(dict_sales, start_date, end_date, expected_result):
    result = validate_sales_dates_within_simulation_period(dict_sales, start_date, end_date)
    assert result == expected_result

# Test case 2: Some sales dates are before the simulation period
dict_sales_invalid_dates_before = {
    'Store1': ['2021-12-30', '2022-01-01', '2022-01-02'],
    'Store2': ['2022-01-01', '2022-01-02', '2022-01-03'],
}
start_date_invalid_before = '2022-01-01'
end_date_invalid_before = '2022-01-03'
@pytest.mark.parametrize("dict_sales, start_date, end_date, expected_result", [
    (dict_sales_invalid_dates_before, start_date_invalid_before, end_date_invalid_before, False),
])

def test_validate_sales_dates_within_simulation_period_invalid_dates_before(dict_sales, start_date, end_date, expected_result):
    result = validate_sales_dates_within_simulation_period(dict_sales, start_date, end_date)
    assert result == expected_result

# Test case 3: Some sales dates are after the simulation period
dict_sales_invalid_dates_after = {
    'Store1': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Store2': ['2022-01-01', '2022-01-02', '2022-01-04'],
}
start_date_invalid_after = '2022-01-01'
end_date_invalid_after = '2022-01-03'
@pytest.mark.parametrize("dict_sales, start_date, end_date, expected_result", [
    (dict_sales_invalid_dates_after, start_date_invalid_after, end_date_invalid_after, False),
])

def test_validate_sales_dates_within_simulation_period_invalid_dates_after(dict_sales, start_date, end_date, expected_result):
    result = validate_sales_dates_within_simulation_period(dict_sales, start_date, end_date)
    assert result == expected_result

# Run the tests
if __name__ == '__main__':
    pytest.main()

