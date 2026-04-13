# Stock Portfolio Tracker
#### Description:
### Overview:

This project is a Python based stock portfolio analysis tool that allows users to create and manage a personal stock portfolio. Users can add or remove investments by stock symbol and quantity, and the program calculates portfolio value and performance using recent market data.
The application presents results in a clear, tabulated portfolio summary showing individual stock holdings and overall portfolio performance, making it easy to track investment results in one place.

### Key Features:

•	Add and remove stock holdings by symbol and quantity
•	Fetch recent market prices using an external API
•	Calculate portfolio metrics including total value, dollar return,  and percentage return
•	Display a consolidated portfolio summary table with per stock and total performance
•	Persist user portfolio data locally using JSON storage
•	Support multiple user portfolios identified by name

### Technologies Used:

•	**Python**
•	**requests** (API data retrieval)
•	**tabulate** (formatted console output)
•	**JSON** (local data persistence)

### What This Project Demonstrates:

This project demonstrates applied financial analysis and practical Python development, including:
•	Working with external APIs and managing rate limits
•	Data manipulation and calculation of financial metrics (returns, portfolio value)
•	Designing persistent data storage for user specific data
•	Writing modular functions for calculations, data handling, and display logic
•	Implementing basic testing to validate calculation accuracy

### Project Structure:

•	project.py – Main application logic, including portfolio management, calculations, API integration, and display
•	test_project.py – Unit tests for portfolio calculation functions
•	requirements.txt – Required third party libraries

### Notes: 

•	The project fetches prices based on the most recent market close due to API usage limits.
•	An internal price cache is used to avoid redundant API calls during a single run.

### Background: 

Originally developed as a final project for a Python programming course, and later refined for portfolio and professional use.