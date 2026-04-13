import requests
import json
import os
from tabulate import tabulate

green = "\033[92m"
red = "\033[91m"
reset = "\033[0m"
price_cache = {}


def calculate_total_invested(portfolio):
    total = 0.0
    for stock in portfolio.values():
        quantity = stock["quantity"]
        avg_price = stock["avg_price"]
        total += quantity * avg_price
    return round(total, 2)


def calculate_total_value(portfolio, stock_prices):
    total = 0.0
    for symbol, stock in portfolio.items():
        quantity = stock["quantity"]
        price = stock_prices[symbol]
        total += quantity * price
    return round(total, 2)


def calculate_total_gain_loss(total_invested, total_value):
    return round((total_value - total_invested), 2)


def load_data():
    try:
        with open("portfolios.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_data(data):
    with open("portfolios.json", "w") as file:
        json.dump(data, file)


def fetch_price(stock):
    if stock in price_cache:
        return price_cache[stock]
    try:
        stock_data = requests.get(
            f"https://api.massive.com/v2/aggs/ticker/{stock}/prev?adjusted=true&apiKey=Imu9ISv2dQmd4Rp7gDeWli1p2jB1uzB1"
        ).json()
        if not stock_data["status"] == "OK":
            raise ValueError("Request Failed")
        if "results" not in stock_data:
            raise ValueError("Invalid stock")
        price_cache[stock] = float(stock_data["results"][0]["c"])
        return float(stock_data["results"][0]["c"])
    except requests.RequestException:
        raise ValueError("Network Error. Try Again.")


def add_investment(portfolio):
    stock = input("What stock would you like to add? ")
    try:
        quantity = float(input(f"What quantity of {stock} are you adding? "))
        price = float(input("At what price? $"))
    except ValueError:
        print("Invalid quantity or price. Please try again")
        input("Press Enter to continue.")
        return
    if price < 0:
        print("Price must be positive. Please try again.")
        input("Press Enter to continue.")
        return
    try:
        fetch_price(stock)
    except ValueError:
        print("Invalid Stock. Please try again.")
        input("Press Enter to continue.")
        return
    if quantity <= 0:
        print("Quantity must be positive. Please try again.")
        input("Press Enter to continue.")
        return
    if stock in portfolio:
        original_quantity = portfolio[stock]["quantity"]
        adding_quantity = quantity
        old_price = portfolio[stock]["avg_price"]
        new_price = price
        new_avg_price = (
            (original_quantity * old_price) + (adding_quantity * new_price)
        ) / (original_quantity + adding_quantity)
        new_quantity = adding_quantity + original_quantity
        portfolio[stock] = {"quantity": new_quantity, "avg_price": new_avg_price}
    else:
        portfolio[stock] = {"quantity": quantity, "avg_price": price}


def remove_investment(portfolio):
    stock = input("What stock would you like to remove? ")
    if stock in portfolio:
        quantity = float(input(f"What quantity of {stock} are you removing? "))
        if quantity > portfolio[stock]["quantity"]:
            print("Cannot remove more shares than owned. Please try again.")
            input("Press Enter to continue.")
            return
        elif quantity <= 0:
            print("Quantity must be positive. Please try again.")
            input("Press Enter to continue.")
            return
    else:
        print("Stock not found. Please try again.")
        input("Press Enter to continue.")
        return
    original_quantity = portfolio[stock]["quantity"]
    remove_quantity = quantity
    new_quantity = original_quantity - remove_quantity
    portfolio[stock]["quantity"] = new_quantity
    if portfolio[stock]["quantity"] == 0:
        del portfolio[stock]

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def display_portfolio(portfolio):
    if not portfolio:
        print("No portfolio on file.")
    else:

        stock_prices = {}

        for stock in portfolio:
            price = fetch_price(stock)
            stock_prices[stock] = price

        total_invested = calculate_total_invested(portfolio)
        total_value = calculate_total_value(portfolio, stock_prices)
        total_gain_loss = calculate_total_gain_loss(total_invested, total_value)
        if total_invested == 0:
            total_percent_gain_loss = 0
        else:
            total_percent_gain_loss = (total_gain_loss / total_invested) * 100

        if total_gain_loss < 0:
            total_gain_loss = f"{red}-${abs(total_gain_loss):.2f}{reset}"
        elif total_gain_loss > 0:
            total_gain_loss = f"{green}${total_gain_loss:.2f}{reset}"
        else:
            total_gain_loss = f"${total_gain_loss:.2f}"
        if total_percent_gain_loss < 0:
            total_percent_gain_loss = f"{red}{total_percent_gain_loss:.2f}%{reset}"
        elif total_percent_gain_loss > 0:
            total_percent_gain_loss = f"{green}{total_percent_gain_loss:.2f}%{reset}"
        else:
            total_percent_gain_loss = f"{total_percent_gain_loss:.2f}%"

        table = []
        headers = [
            "Symbol",
            "Quantity",
            "Avg. Price",
            "Last Price",
            "Current Value",
            "$ Gain/Loss",
            f"% Gain Loss",
        ]
        totals = [
            "Total",
            "",
            "",
            "",
            f"${total_value:.2f}",
            total_gain_loss,
            total_percent_gain_loss,
        ]
        for stock in portfolio:
            avg_price = portfolio[stock]["avg_price"]
            quantity = portfolio[stock]["quantity"]
            last_price = stock_prices[stock]

            invested = avg_price * quantity
            current_value = quantity * last_price
            dollar_gain_loss = current_value - invested
            if invested == 0:
                percent_gain_loss = 0
            else:
                percent_gain_loss = (dollar_gain_loss / invested) * 100
            if dollar_gain_loss < 0:
                dollar_gain_loss = f"{red}-${abs(dollar_gain_loss):.2f}{reset}"
            elif dollar_gain_loss > 0:
                dollar_gain_loss = f"{green}${dollar_gain_loss:.2f}{reset}"
            else:
                dollar_gain_loss = f"${dollar_gain_loss:.2f}"
            if percent_gain_loss < 0:
                percent_gain_loss = f"{red}{percent_gain_loss:.2f}%{reset}"
            elif percent_gain_loss > 0:
                percent_gain_loss = f"{green}{percent_gain_loss:.2f}%{reset}"
            else:
                percent_gain_loss = f"{percent_gain_loss:.2f}%"

            row = [
                stock,
                portfolio[stock]["quantity"],
                f"${portfolio[stock]["avg_price"]:.2f}",
                f"${stock_prices[stock]:.2f}",
                f"${current_value:.2f}",
                dollar_gain_loss,
                percent_gain_loss,
            ]
            table.append(row)
        table.append(totals)
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def main():
    data = load_data()
    username = input("Welcome to Stock Investment Tracker. Please enter your name? ").strip()
    if username not in data:
        create = (
            input(
                f"Hello {username}. There is no portfolio under that name. Would you like to create one? (y/n): "
            )
            .strip()
            .lower()
        )
        if create == "y":
            data[username] = {}
            save_data(data)
        else:
            return
    else:
        print(f"Welcome Back, {username}.")
    while True:
        portfolio = data[username]
        clear_screen()
        display_portfolio(portfolio)
        add_remove = (
            input("Would you like to make changes? (Add/Remove/Exit): ").strip().lower()
        )
        if add_remove == "add":
            add_investment(portfolio)
            save_data(data)
        elif add_remove == "remove":
            remove_investment(portfolio)
            save_data(data)
        elif add_remove == "exit":
            break
        else:
            print("Invalid input. Please try again.")
            input("Press Enter to continue.")


if __name__ == "__main__":
    main()
