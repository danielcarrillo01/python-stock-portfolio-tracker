from project import calculate_total_invested
from project import calculate_total_value
from project import calculate_total_gain_loss


def test_calculate_total_invested():
    portfolio = {
        "NVDA" : {"quantity" : 5,"avg_price" : 150.30},
        "AAPL" : {"quantity" : 10,"avg_price" : 200.59},
        "MSFT" : {"quantity" : 12,"avg_price" : 309.67},
        "AMZN" : {"quantity" : 5.7,"avg_price" : 169.70}
    }

    assert calculate_total_invested(portfolio) == 7440.73

    portfolio = {}

    assert calculate_total_invested(portfolio) == 0


def test_calculate_total_value():
    portfolio = {
        "NVDA" : {"quantity" : 5,"avg_price" : 149.27},
        "AAPL" : {"quantity" : 39,"avg_price" : 198.80},
        "MSFT" : {"quantity" : 10,"avg_price" : 300.78},
        "AMZN" : {"quantity" : 8,"avg_price" : 100.76}
    }
    stock_prices = {
        "NVDA" : 182.37,
        "AAPL" : 264.72,
        "MSFT" : 398.55,
        "AMZN" : 208.20
    }

    assert calculate_total_value(portfolio,stock_prices) == 16887.03

    portfolio = {}
    stock_prices = {}

    assert calculate_total_value(portfolio,stock_prices) == 0

def test_caluclate_total_gain_loss():
    assert calculate_total_gain_loss(16987.67,34876.15) == 17888.48
    assert calculate_total_gain_loss(56827.87,39658.05) == -17169.82
    assert calculate_total_gain_loss(40876.88,40876.88) == 0
