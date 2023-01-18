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

        data_str = input(("Enter your data here:\n "))
        # convert string data to list
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


def get_last_5_entries_sales():
    """ Collecting the last 5 entries from each coumn of data.
        Returning a list of lists
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def update_worksheet(data, worksheet):
    """
    Recieves a list of integers to be inserted to a worksheet.
    """
    print(f"Updating sales {worksheet} ...\n")
    worksheet_to_update = SHEET.worksheet(f'{worksheet}')
    worksheet_to_update.append_row(data)
    print(f"{worksheet} work sheet updated successfully.\n")


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


def calculate_stock_data(data):
    """ Calculate the average of each stock type and add 10% to it """
    print("Calculating stock data ...\n")
    new_stock_data = []
    for column in data:
        int_col = [int(col) for col in column]
        average = sum(int_col)/len(int_col)
        stock_num = average*1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data



def main():
    """ Run all program functions. """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    stock_column = get_last_5_entries_sales()
    stock_data = calculate_stock_data(stock_column)
    update_worksheet(stock_data, 'stock')
    
    




print("Welcome to Love Sandwiches Data Automation. ")

main()
