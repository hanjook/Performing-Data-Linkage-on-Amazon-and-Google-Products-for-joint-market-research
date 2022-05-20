# Dependencies
- Language: python
- Packages / Libraries: fuzzywuzzy, pandas
# Data:
- provided by the University of Melbourne, not sure about the exact source
# Directory
- `data`: contains the products and their description
- `Analysis`: explains the approach of data linkage and includes the analysis performed on the precision and accuracy of the data linkage with and without blocking
- `Perform_blocking`: performs blocking on the amazon.csv and google.csv files based on the words with more than 1 frequency in the product descriptions
- `link_data_files`: links the amazon.csv and google.csv products by the highest scoring pair when using fuzzywuzzy on the product descriptions
