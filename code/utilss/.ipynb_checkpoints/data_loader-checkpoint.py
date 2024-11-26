import pandas as pd

def load_data(filepath="C:/Users/amanp/Desktop/MINOR/proj/code/dataset/Brazil_UF_dengue_monthly.csv"):
    """
    Loads the dataset from a CSV file.
    """
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError:
        raise FileNotFoundError("The data file was not found. Please check the filepath.")
