# Test_case_scrapper
This project is a Test case scraper that extracts tables (testcase) from an HTML file and writes it to an Excel file. The project is written in Python and uses the BeautifulSoup and Pandas libraries.

**Usage:**

To use the scraper, you must have Python 3 and the following libraries installed:

1. BeautifulSoup4
2. Pandas
3. openpyxl

Before ruuning the  scraper, Provide the file path of the html file

To run the scraper, simply execute the scraper.py file in your terminal:

`python scraper.py`

The scraper  will extract the testcase from the html-table and save it to an Excel file .

**Customization :**

The scraper is designed to work with Matter-specific HTML tables that have a specific structure. If the table has a different structure, you may need to modify the scraper code to extract the data correctly.

The scraper also includes some options for customizing the output. For example, you can change the column and row in the Excel file by modifying in the scraper.py file.

**Credits** 

This project was created by SAravana perumal K. The web scraper was built using the BeautifulSoup and Pandas libraries, which are maintained by the following developers:

- BeautifulSoup: Leonard Richardson 
- Pandas: Wes McKinney
