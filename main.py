import pandas as pd
import numpy as np

def check_missing_values(df):
    missing_data = df.isnull()
    for column in missing_data.columns.values.tolist():
        print(column)
        print (missing_data[column].value_counts())
        print("")
def clean_data(df):
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.replace("?", np.NaN)
    return df

def replace_missing_values(df):


    avg_norm_loss = df["normalized-losses"].astype("float").mean(axis=0)
    avg_bore = df['bore'].astype('float').mean(axis=0)
    avg_horsepower = df['horsepower'].astype('float').mean(axis=0)
    avg_peakrpm = df['peak-rpm'].astype('float').mean(axis=0)
    max_doors = df['num-of-doors'].value_counts().idxmax()
    avg_stroke = df["stroke"].astype("float").mean(axis=0)


    df["normalized-losses"].replace(np.NaN, avg_norm_loss, inplace=True)
    df['horsepower'].replace(np.NaN, avg_horsepower,inplace=True)
    df['peak-rpm'].replace(np.NaN, avg_peakrpm,inplace=True)
    df["num-of-doors"].replace(np.NaN, max_doors,inplace=True)
    df["bore"].replace(np.nan, avg_bore, inplace=True)
    df['stroke'].replace(np.nan, avg_stroke,inplace=True)
    print(df.at[8,'price'])
    print(df["price"].isnull().sum())
    df.dropna(subset=["price"], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def fix_data_types(df):
    df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
    df[["normalized-losses","horsepower"]] = df[["normalized-losses","horsepower"]].astype("int")
    df[["price"]] = df[["price"]].astype("float")
    df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")
    return df

def normalize(df):
    df['length'] = df['length'] / df['length'].max()
    df['width'] = df['width'] / df['width'].max()
    df['height'] = df['height'] / df['height'].max()
    print(df[['length','width','height']].head())
    return df

def bin(df):
    bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]), 4)
    group_names = ['Low', 'Medium', 'High']
    df['horsepower-binned'] = pd.cut(df['horsepower'], bins, labels=group_names, include_lowest=True)
    horsepower_index = df.columns.get_loc('horsepower')
    new_columns = df.columns.tolist()
    new_columns = new_columns[:horsepower_index + 1] + ['horsepower-binned'] + new_columns[horsepower_index + 1:-1]
    df = df[new_columns]
    return df

def main():
    df = pd.read_csv("imports-85.csv")

    headers = ["symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors", "body-style",
               "drive-wheels", "engine-location", "wheel-base", "length", "width", "height", "curb-weight",
               "engine-type",
               "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke", "compression-ratio", "horsepower",
               "peak-rpm", "city-mpg", "highway-mpg", "price"]
    df.columns = headers
    df.to_csv("dataset_with_columns.csv", index=False)
    df = clean_data(df)
    check_missing_values(df)
    df.to_csv("dataset_after_NaN.csv",index=False)
    df.describe(include="all").to_csv("statistics.csv")
    df = replace_missing_values(df)
    df = fix_data_types(df)
    check_missing_values(df)
    df = normalize(df)
    df = bin(df)
    df.to_csv("Cleaned.csv",index=False)
main()
