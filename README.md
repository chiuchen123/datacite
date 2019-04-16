# DataCite Repository

Python scripts to help researchers submit valid XML documents to DataCite to create DOIs and their metadata.  

## dataCiteExcelToXML.py
This script creates well-formed XML documents for importation into [DataCite](https://datacite.org/index.html) from an Excel workbook.

The script first combines metadata in the Excel sheets into an easily-readable CSV using the Python [pandas library](https://pandas.pydata.org/pandas-docs/stable/index.html) and the [xlrd package](https://pypi.org/project/xlrd/). (An example of the Excel workbook with sample metadata is available in this repository and is called exampleDataCiteSubmission.xlsx.)

The script then creates one or many XML documents from the CSV based on the request number  field, using the [lxml](https://lxml.de/index.html) package and [CSV module](https://docs.python.org/3/library/csv.html#module-csv). Each unique request number creates a corresponding XML document. The XML documents are formed to adhere to the [DataCite Metadata Schema 4.2](https://schema.datacite.org/).
