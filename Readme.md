# Primetrade.ai Assignment

## Overview
This repository contains a Python-based application to track cryptocurrency data in real-time using the CoinGecko API. The application fetches details about the top 50 cryptocurrencies, serves the data through an HTTP server, and provides a dynamic HTML template for live updates and visualization.

---

## Features
- Fetches real-time data of the top 50 cryptocurrencies, including:
  - Name, Symbol, Current Price (USD), Market Capitalization, 24h Trading Volume, and Price Change (24h %).
- Hosts a local HTTP server to serve the cryptocurrency data as JSON.
- Provides an auto-updating HTML dashboard for visualization.
- Supports integration with Microsoft Excel for live data tracking.

---

## Prerequisites
To run this project, ensure you have the following installed:

- **Python** (version >= 3.7)
- **Pandas** and **Requests** libraries
- **OpenPyxl** library

---

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/i3hz/Primetrade.ai-assignment.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Primetrade.ai-assignment
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage for crypto_live_webpage.py
1. Start the application:
    ```bash
    python crypto_live_webpage.py
    ```

2. Open the `crypto_live_data.html` file in your browser to see live cryptocurrency updates.

3. For Microsoft Excel integration:
    - Open Excel.
    - Go to **Data -> Get Data -> From Web**.
    - Enter the URL: `http://localhost:8000`.
    - Set the refresh rate in **Data -> Properties**.

---
## Usage for excel_save.py
1. Start the application:
    ```bash
    python excel_save.py
### Output
The script creates/updates an Excel file named crypto_live_data.xlsx with three sheets:

    Live Data: Contains the top 50 cryptocurrencies with their current price, market capitalization, trading volume, and price change over the last 24 hours.
    Analysis: Displays key analysis like the average price, highest/lowest 24h price change, and top 5 by market cap.
    Top 5 by Market Cap: Lists the top 5 cryptocurrencies by market cap.    ```


---
## File Structure
- `crypto_live_webpage.py`: Main script containing the logic for fetching data, starting the server, and generating the HTML file.
- `excel_save.py` : Script which saves the fetched data in excel format and updates the said excel file every 300 seconds(or 5 minutes).
- `crypto_live_data.html`: Auto-generated HTML dashboard for live updates.
- `requirements.txt`: List of dependencies.

---

## How It Works
1. The script fetches real-time cryptocurrency data every 30 seconds from the CoinGecko API.
2. A local HTTP server serves the data as JSON at `http://localhost:8000`.
3. The HTML dashboard dynamically updates using JavaScript to fetch data from the server.
4. Users can integrate the live data into Excel using the web query feature.

---

## Contribution Guidelines
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes and push to your fork.
4. Submit a pull request detailing your changes.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contact
For questions or suggestions, please reach out to:
- **Author**: i3hz
- **Email**: [vedthorat1029@gmail.com.com]
- **GitHub Profile**: [github.com/i3hz]

