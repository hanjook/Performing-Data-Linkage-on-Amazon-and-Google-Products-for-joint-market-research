# Dependencies
- Language: python
- Packages / Libraries: fuzzywuzzy, pandas
# Directory
- 'Analysis': explaing the approach of data linkage and analysis performed on the precision and accuracy of the data linkage with and without blocking
- 'Perform_blocking': performs blocking on the amazon.csv and google.csv files based on the words with more than 1 frequency in the product descriptions
- 'link_data_files': links the amazon.csv and google.csv products by the highest scoring pair when using fuzzywuzzy on the product descriptions
