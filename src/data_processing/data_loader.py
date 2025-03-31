import os
import pandas as pd

def load_om_stats():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/om/stats_om.csv")
    return pd.read_csv(data_path)

def load_psg_stats():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/psg/stats_psg.csv")
    return pd.read_csv(data_path)

if __name__ == "__main__":
    print("OM Stats:")
    print(load_om_stats().head())
    print("PSG Stats:")
    print(load_psg_stats().head())