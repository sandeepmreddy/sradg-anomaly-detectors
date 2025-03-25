import pandas as pd

# Load the CSV file
file_path = "AnamolyCase1.csv"  # Update path if needed
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

# Convert numeric columns
df["Ihub Balance"] = pd.to_numeric(df["Ihub Balance"], errors='coerce')
df["GL  balance"] = pd.to_numeric(df["GL  balance"], errors='coerce')

# Compute the difference
df["Difference"] = df["Ihub Balance"] - df["GL  balance"]

# Sort by account and date
df.sort_values(by=["Account Number", "As of Date"], inplace=True)

# Function to detect anomalies for each account
def detect_anomaly(group):
    # Historical differences except the last row
    if len(group) > 1:
        historical_zero = (group["Difference"].iloc[:-1] == 0).all()
        latest_non_zero = group["Difference"].iloc[-1] != 0
        is_anomaly = historical_zero and latest_non_zero
    else:
        is_anomaly = False  # Not enough data to determine anomaly

    group["isAnomaly"] = is_anomaly
    return group

# Apply anomaly detection
df = df.groupby("Account Number", group_keys=False).apply(detect_anomaly)

# Drop duplicates to get one row per account (you can adjust this if needed)
summary = df.drop_duplicates(subset=["Account Number"])[["Account Number", "Match Status", "isAnomaly"]]

# Display the result
print("\nAccount Anomaly Summary:")
print(summary.to_string(index=False))
