import pytest
from datetime import datetime
from fashion_strategy.simulation.generalization_version_factory.preprocess import create_fix_start_dates


# Test case 1: Empty start_dates and end_dates
start_dates_empty = {}
end_dates_empty = {}
expected_output_empty = {}
def test_create_fix_start_dates_empty():
    result = create_fix_start_dates(start_dates_empty, end_dates_empty)
    assert result == expected_output_empty

# Test case 2: Only one SKU in end_dates
start_dates_single_sku = {
    '2022-01-01': [('SKU1', 'Store1')],
    '2022-01-02': [('SKU1', 'Store2')],
}
end_dates_single_sku = {
    '2022-01-01': ['SKU1'],
}
expected_output_single_sku = {
    '2022-01-01': [('SKU1', 'Store1')],
}
def test_create_fix_start_dates_single_sku():
    result = create_fix_start_dates(start_dates_single_sku, end_dates_single_sku)
    assert result == expected_output_single_sku

# Test case 3: SKU with multiple end dates
start_dates_multiple_end_dates = {
    '2022-01-01': [('SKU1', 'Store1'), ('SKU2', 'Store2')],
    '2022-01-02': [('SKU1', 'Store2')],
}
end_dates_multiple_end_dates = {
    '2022-01-01': ['SKU1'],
    '2022-01-02': ['SKU2'],
}
expected_output_multiple_end_dates = {'2022-01-01': [('SKU1', 'Store1'), ('SKU2', 'Store2')]}
def test_create_fix_start_dates_multiple_end_dates():
    result = create_fix_start_dates(start_dates_multiple_end_dates, end_dates_multiple_end_dates)
    assert result == expected_output_multiple_end_dates

# Test case 4: No SKUs in start_dates after filtering
start_dates_no_skus_left = {
    '2022-01-04': [('SKU1', 'Store1'), ('SKU2', 'Store2')],
    '2022-01-05': [('SKU1', 'Store2')],
}
end_dates_no_skus_left = {
    '2022-01-01': ['SKU1'],
    '2022-01-02': ['SKU2'],
}
expected_output_no_skus_left = {}
def test_create_fix_start_dates_no_skus_left():
    result = create_fix_start_dates(start_dates_no_skus_left, end_dates_no_skus_left)
    assert result == expected_output_no_skus_left

# Test case 5: All SKUs have end dates after start dates
start_dates_all_skus_left = {
    '2022-01-01': [('SKU1', 'Store1')],
    '2022-01-02': [('SKU1', 'Store2')],
}
end_dates_all_skus_left = {
    '2022-01-09': ['SKU1'],
}
expected_output_all_skus_left = {
    '2022-01-01': [('SKU1', 'Store1')],
    '2022-01-02': [('SKU1', 'Store2')],
}
def test_create_fix_start_dates_all_skus_left():
    result = create_fix_start_dates(start_dates_all_skus_left, end_dates_all_skus_left)
    assert result == expected_output_all_skus_left

# Run the tests
if __name__ == '__main__':
    test_create_fix_start_dates_empty()
    test_create_fix_start_dates_single_sku()
    test_create_fix_start_dates_multiple_end_dates()
    test_create_fix_start_dates_no_skus_left()
    test_create_fix_start_dates_all_skus_left()


