def clean_data(df):
    df.columns = [col.strip().lower() for col in df.columns]
    return df

if __name__ == "__main__":
    import pandas as pd
    df = pd.DataFrame({" Column1 ": [1, 2, 3], " Column2 ": ["a", "b", "c"]})
    print("Avant nettoyage:", df.columns)
    df_clean = clean_data(df)
    print("Après nettoyage:", df_clean.columns)