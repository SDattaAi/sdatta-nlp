import pytest
from fashion_strategy.simulation.generalization_version_factory.input_dicts_validation import validate_stock_zero_for_warehouse

# Test case 1: Warehouse store is in dict_stocks with zero stock
dict_stocks_case1 = {'VZ01': {'SKU1': 0, 'SKU2': 0}}
def test_validate_stock_zero_for_warehouse_case1():
    result = validate_stock_zero_for_warehouse(dict_stocks_case1)
    assert result == False

# Test case 2: Warehouse store is in dict_stocks with non-zero stock
dict_stocks_case2 = {'VZ01': {'SKU1': 100, 'SKU2': 200}}
def test_validate_stock_zero_for_warehouse_case2():
    result = validate_stock_zero_for_warehouse(dict_stocks_case2)
    assert result == True

# Test case 3: Warehouse store is not in dict_stocks
dict_stocks_case3 = {'Store1': {'SKU1': 100, 'SKU2': 200}}
def test_validate_stock_zero_for_warehouse_case3():
    result = validate_stock_zero_for_warehouse(dict_stocks_case3)
    assert result == True

# Test case 4: Warehouse store is in dict_stocks with a mix of zero and non-zero stock
dict_stocks_case4 = {'VZ01': {'SKU1': 0, 'SKU2': 100, 'SKU3': 0}, 'Store1': {'SKU1': 0, 'SKU2': 0}}
def test_validate_stock_zero_for_warehouse_case4():
    result = validate_stock_zero_for_warehouse(dict_stocks_case4)
    assert result == False




# Test case 5: Warehouse store is in dict_stocks with zero stock but other stores have non-zero stock
dict_stocks_case5 = {'VZ01': {'SKU1': 0, 'SKU2': 0}, 'Store1': {'SKU1': 100, 'SKU2': 200}}
def test_validate_stock_zero_for_warehouse_case5():
    result = validate_stock_zero_for_warehouse(dict_stocks_case5)
    assert result == False

# Test case 6: Warehouse store is in dict_stocks with non-zero stock and other stores have zero stock
dict_stocks_case6 = {'VZ01': {'SKU1': 100, 'SKU2': 200}, 'Store1': {'SKU1': 0, 'SKU2': 0}}
def test_validate_stock_zero_for_warehouse_case6():
    result = validate_stock_zero_for_warehouse(dict_stocks_case6)
    assert result == True

dict_stocks_case7 = {'VZ01': {'SKU1': 100, 'SKU2': 100, 'SKU3': 100}, 'Store1': {'SKU1': 1, 'SKU2': 2}}
def test_validate_stock_zero_for_warehouse_case7():
    result = validate_stock_zero_for_warehouse(dict_stocks_case7)
    assert result == True

# Run the tests
if __name__ == '__main__':
    test_validate_stock_zero_for_warehouse_case1()
    test_validate_stock_zero_for_warehouse_case2()
    test_validate_stock_zero_for_warehouse_case3()
    test_validate_stock_zero_for_warehouse_case4()
    test_validate_stock_zero_for_warehouse_case5()
    test_validate_stock_zero_for_warehouse_case6()
    test_validate_stock_zero_for_warehouse_case7()
