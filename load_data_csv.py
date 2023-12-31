import pandas as pd
import os

datasets_name = ['e-tax-service', 'patent_tax', 'registration_tax', 'specific_tax',
                 'tax_on_property_rental', 'tax_on_property', 'tax_on_salary', 'tax_on_transportation', 'tax_on_unused_land', 'vat', 'withholding_tax', "taxpayer"]

datasets_dir = "datasets"
output_file = "tax_data.csv"


def convert_and_merge_data():
    df_tax = pd.concat([pd.read_json(os.path.join(datasets_dir, f"{i}.json"))
                        .drop('tagKH', axis=1) if i == "taxpayer"
                        else pd.read_json(os.path.join(datasets_dir, f"{i}.json"))
                        for i in datasets_name], ignore_index=True)

    df_tax.to_csv(output_file, index=False)
    print("Conversion and Merging completed.")


def clean_data():
    try:
        df = pd.read_csv(output_file)
        df_cleaned = df[df.pattern != "[]"]
        df_cleaned.to_csv(output_file, index=False)
        print("Clean Data: Completed")
    except FileNotFoundError:
        print(f"Error: File '{output_file}' not found.")


def filter_data():
    def manipulate(text):
        text = text.lower()
        if 'e-filing' in text:
            return text
        return text.replace('-', ' ')
    df = pd.read_csv("tax_data.csv")
    df.intent = df.intent.apply(manipulate)
    df.to_csv("tax_data.csv", index=False)
    print("Filter Data: Completed")


def wrangle_tax_data(data_path="tax_data.csv"):
    df = pd.read_csv(data_path)
    ls = []
    for _, row in df.iterrows():
        patterns = row["pattern"].split(", ")
        for pattern in patterns:
            pattern = "".join(
                [c for c in pattern if c not in [
                    "[", "]", "'", "\\", "u", "2", "0", "b"]]
            )
            new_row = {
                "intent": row["intent"],
                "pattern": pattern,
                "response": row["responses"],
            }
            ls.append(new_row)

    df_tax = pd.DataFrame(ls, columns=[
        'intent', 'pattern', 'response'])
    df_tax["response"] = df_tax.response.str.replace(
        r"\[|\]|\'+|\"+", "", regex=True
    )
    df_tax.to_csv(data_path, index=False)
    print("Wrangle Data: Completed")

# def merge_csv():
#     df_tax = pd.DataFrame()
#     for i in datasets_name:
#         individual_tax_file = f"{i}.csv"
#         df_specific_tax = pd.read_csv(individual_tax_file)
#         df_tax = pd.concat([df_tax, df_specific_tax], ignore_index=True)
#         if os.path.exists(individual_tax_file):
#             os.remove(individual_tax_file)
#     df_tax.to_csv("tax_data.csv", index=False)
#     print("Merged Data: Completed")


convert_and_merge_data()
clean_data()
filter_data()
wrangle_tax_data()
