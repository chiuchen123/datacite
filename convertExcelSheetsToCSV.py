import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Enter Excel filename to convert to CSV, including extension. Optional - if not provided, the script will ask for input. Example: sheets.xlsx')
parser.add_argument('-s', '--save', help="Enter file path with filename where you'd like CSV saved. Optional - if not provided, the script will ask for input. Example: C:\\Users\\User1\\Desktop\\export_dataframe.csv")
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = raw_input('Enter Excel filename: ')
if args.save:
    filepath = args.save
else:
    filepath = raw_input('Enter file path: ')

# Create the pd.ExcelFile() object
xls = pd.ExcelFile(filename)

# Extract the sheet names from xls
sheetNamesList = xls.sheet_names
sheetNamesList.pop()
print(sheetNamesList)

# Create an empty list: listings
listings = []

# Import the data
for sheetName in sheetNamesList :
    df = pd.read_excel(xls, sheet_name=sheetName, na_values='n/a')
    df = df.iloc[1:,:]
    df.dropna(axis=0, how='all', thresh=None, subset=None, inplace=True)
    df.dropna(axis=1, how='all', thresh=None, subset=None, inplace=True)
    #print df
    listings.append(df)

# Concatenate the listings: listing_data
listing_data = pd.concat(listings, join ='outer', ignore_index=True, sort=False)
listing_data.to_csv(filepath, index = False, header = True, encoding = 'utf-8')
