def test_update_stocks_by_sales():
    dict_stocks = {'store1': {101: 70}, 'store2': {101: 60}}
    dict_sales = {'store1': {'2024-01-02': [(101, 30)]}, 'store2': {'2024-01-02': [(101, 70)]}}
    MissedSales = {'store1': {101: 0}, 'store2': {101: 0}}
    date = '2024-01-02'
    updated_stocks, updated_missed_sales = update_stocks_by_sales(dict_stocks, dict_sales, MissedSales, date)
    assert updated_stocks['store1'][101] == 40
    assert updated_stocks['store2'][101] == 0
    assert updated_missed_sales['store1'][101] == 0
    assert updated_missed_sales['store2'][101] == 10