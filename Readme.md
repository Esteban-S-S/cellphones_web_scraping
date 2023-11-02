
# Web Scraping of Cellphone Products in Argentina

This project performs web scraping on the online stores of three websites in Argentina to gather information about available cellphones in their catalogs. It uses Python libraries such as `requests`, `BeautifulSoup`, `random`, `time`, `pandas`, and `selenium` to automate the data extraction process.

## Description

The main objective of this project is to obtain detailed information about the cellphones available in the online stores of Argentina. This includes data such as the phone model, price, technical specifications, and more.

## Requirements

The following Python libraries should be installed in your environment:

- `requests`
- `BeautifulSoup`
- `random`
- `time`
- `pandas`
- `selenium`
- `lxml`

Additionally, you'll need the Chrome driver for Selenium.

## Additional Notes

- This project is conducted for educational and learning purposes regarding web scraping and web automation with publicly available data.

- Each script has a corresponding Jupyter notebook file to monitor script performance. Create a DataFrame for critical errors, such as missing model name or product price. If there are more than 10 critical errors, it indicates a serious problem and code execution is stopped. In case the errors are not critical, such as missing data from the processor, store the product link in the "errors" column for later analysis.

- In the case of .py files, when it finds more than 10 critical errors per terminal, it sends a message proposing to stop the script by pressing Ctrl + C.

- Random wait times have been incorporated to avoid overloading servers and to simulate more human-like behavior.