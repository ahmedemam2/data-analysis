import pandas as pd
import numpy as np

def identify_missing_values(df):
    df_replaced = df.replace("?", np.NaN)
    missing_data = df.isnull()
    for column in missing_data.columns.values.tolist():
        print(column)
        print (missing_data[column].value_counts())
        print("")
    return df

def replace_missing_values(df):
    df.dropna(subset=["price"], axis=0)
    df.reset_index(drop=True)
    df.to_csv("bgrb.csv")
    avg_norm_loss = df["normalized-losses"].astype("float").mean(axis=0)
    print("Average of normalized-losses:", avg_norm_loss)
    df["normalized-losses"].replace(np.NaN, avg_norm_loss, inplace=True)
    avg_bore = df['bore'].astype('float').mean(axis=0)
    print("Average of bore:", avg_bore)
    df["bore"].replace(np.NaN, avg_bore)
    avg_horsepower = df['horsepower'].astype('float').mean(axis=0)
    print("Average horsepower:", avg_horsepower)
    df['horsepower'].replace(np.NaN, avg_horsepower)
    avg_peakrpm = df['peak-rpm'].astype('float').mean(axis=0)
    print("Average peak rpm:", avg_peakrpm)
    df['peak-rpm'].replace(np.NaN, avg_peakrpm)
    max_doors = df['peak-rpm'].replace(np.nan, avg_peakrpm, inplace=True)
    df["num-of-doors"].replace(np.NaN, max_doors)
    # drop instances where labels don't exist since this is what should be predicted.
    return df

def fix_data_types(df):
    df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
    df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
    df[["price"]] = df[["price"]].astype("float")
    df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")
    return df

def main():
    df = pd.read_csv("imports-85.csv")

    headers = ["symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors", "body-style",
               "drive-wheels", "engine-location", "wheel-base", "length", "width", "height", "curb-weight",
               "engine-type",
               "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke", "compression-ratio", "horsepower",
               "peak-rpm", "city-mpg", "highway-mpg", "price"]
    df.columns = headers
    # create csv file with headers included.
    df.to_csv("dataset_with_columns.csv", index=False)
    # df = df.astype(str)
    df = identify_missing_values(df)
    df.to_csv("dataset_with_columns.csv", index=False)
    # df.describe(include="all").to_csv("statistics.csv")
    df = replace_missing_values(df)
    df = fix_data_types(df)
main()
# df.to_csv("fixedHeader.csv")
