import requests
import pandas as pd


response = requests.get("https://api.mfapi.in/mf/125497")
response.raise_for_status()

data = response.json()
df = pd.DataFrame(data["data"])
df.to_csv("D:/bluestock_mf_capstone/data/raw/live_nav_hdfc_top_100_direct.csv", index=False)

print(df.to_string(index=False))

# SBI Bluechip
response = requests.get("https://api.mfapi.in/mf/119551")
response.raise_for_status()

data_sbi = response.json()
sbi_df = pd.DataFrame(data_sbi["data"])
sbi_df.to_csv("D:/bluestock_mf_capstone/data/raw/live_nav_sbi_bluechip.csv", index=False)

# ICICI Bluechip
response = requests.get("https://api.mfapi.in/mf/120503")
response.raise_for_status()

data_icici = response.json()
icici_df = pd.DataFrame(data_icici["data"])
icici_df.to_csv("D:/bluestock_mf_capstone/data/raw/live_nav_icici_bluechip.csv", index=False)

# Nippon Large Cap
response = requests.get("https://api.mfapi.in/mf/118632")
response.raise_for_status()

data_nippon = response.json()
nippon_df = pd.DataFrame(data_nippon["data"])
nippon_df.to_csv("D:/bluestock_mf_capstone/data/raw/live_nav_nippon_large_cap.csv", index=False)

# Axis Bluechip
response = requests.get("https://api.mfapi.in/mf/119092")
response.raise_for_status()

data_axis = response.json()
axis_df = pd.DataFrame(data_axis["data"])
axis_df.to_csv("D:/bluestock_mf_capstone/data/raw/live_nav_axis_bluechip.csv", index=False)

# Kotak Bluechip
response = requests.get("https://api.mfapi.in/mf/120841")
response.raise_for_status()

data_kotak = response.json()
kotak_df = pd.DataFrame(data_kotak["data"])
kotak_df.to_csv("D:/bluestock_mf_capstone/data/raw/live_nav_kotak_bluechip.csv", index=False)