import pandas as pd

input_filename = "data/yelp_reviews.csv"
output_filename = "data/yelp_reviews_small.csv"
rows_to_keep = 90000

try:
    df = pd.read_csv(input_filename, nrows=rows_to_keep)
    df.to_csv(output_filename, index=False)

    print(
        f"Successfully created '{output_filename}' with the header and first {rows_to_keep} rows."
    )

except FileNotFoundError:
    print(f"Error: The file '{input_filename}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
