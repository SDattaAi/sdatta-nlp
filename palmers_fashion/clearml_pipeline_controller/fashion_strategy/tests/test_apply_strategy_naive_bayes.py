import pytest

# Import the function you want to test
from ... fashion_strategy.simulation.simulation_general import apply_strategy_naive_bayes

# Define some example input data
# vv
current_stock = {
    'store1': {'sku1': 10, 'sku2': 20},
    'store2': {'sku1': 15, 'sku2': 25},
    'VZ01': {'sku1': 10, 'sku2': 20},
}

## vv
AshlonStock = {
    'store1': {'2024-01-01': [('sku1', 5)], '2024-01-02': [('sku2', 10)]},
    'store2': {'2024-01-01': [('sku1', 8)], '2024-01-02': [('sku2', 12)]},
}

# vv
ActiveStores = {'sku1': {'store1': 1, 'store2': 1}, 'sku2': {'store1': 1, 'store2': 0}}

# vv
current_stores_replenished = ['store1', 'store2']

# vv
dict_sales = {
    'store1': {'2024-01-01': [('sku1', 3)], '2024-01-02': [('sku2', 8)]},
    'store2': {'2024-01-01': [('sku1', 5)], '2024-01-02': [('sku2', 10)]},
}

## vv
accumulated_stocks = {
    'store1': {'sku1': 20, 'sku2': 25},
    'store2': {'sku1': 25, 'sku2': 30},
}

date = '2024-01-03'


# Define test cases using pytest.mark.parametrize
@pytest.mark.parametrize(
    "current_stock, AshlonStock, ActiveStores, current_stores_replenished, dict_sales, accumulated_stocks, date, expected_result",
    [
        (current_stock, AshlonStock, ActiveStores, current_stores_replenished, dict_sales, accumulated_stocks, date,
         (current_stock, AshlonStock, accumulated_stocks)),
        # Add more test cases here with different input values and expected results
    ])
def test_apply_strategy_naive_bayes(current_stock, AshlonStock, ActiveStores, current_stores_replenished, dict_sales,
                                    accumulated_stocks, date, expected_result):
    # Call the function with the test inputs
    current_stock, AshlonStock, accumulated_stocks = apply_strategy_naive_bayes(current_stock, AshlonStock, ActiveStores, current_stores_replenished,
                                        dict_sales, accumulated_stocks, date)

    print("current_stock1 = ", current_stock)
    print("AshlonStock1 = ", AshlonStock)
    print("accumulated_stocks1 = ", accumulated_stocks)
    raise NotImplementedError  # Remove this line when you have implemented the function

    # Check if the result matches the expected result
