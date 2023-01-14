import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()


def get_sales_data():
    """
    Get sales figures input from user.
    Run a while loop to collect a valid data
    and returns the valid data.
    """
    while True:

        print("Please enter sales data from the last market")
        print("Data should be six numbers seperated by commas")
        print(("Example: 24,12,15,32,40,60 \n"))

        data_str = input(("Enter your data here: "))
        # conert string data to list
        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(values):
    """
    Raise errors if string cannot be converted to int
    or if there are'nt six values
    """
    try:
        [int(v) for v in values]
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}.")

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True




def update_sales_worksheet(data):
    """
    Update sales worksheet,add new row with the list of data provided
    """
    print("Updating sales worksheet ...\n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Sales work sheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """ Calculate the surplus for each type.
        The surplus is defined as the sales subtracted from the stock.
    """
    print("Calculating the surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock)-sales
        surplus_data.append(surplus)

    return surplus_data


def main():
    """ Run all program functions. """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    




print("Welcome to Love Sandwiches Data Automation. ")
main()