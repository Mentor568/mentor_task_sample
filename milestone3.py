import pandas as pd

def analyze_warehouse_data(file_path):
    # Load the CSV data
    data = pd.read_csv(file_path)

    # Define thresholds and conditions
    warehouse_capacity_threshold = 0.8  # 80% capacity considered high
    risk_threshold = "High"  # Risk levels: Low, Medium, High
    sentiment_threshold = "Negative"  # Sentiment: Positive, Neutral, Negative

    alerts = []

    for index, row in data.iterrows():
        # Calculate warehouse utilization
        utilization = row['Monthly Incoming'] / row['Warehouse Capacity']

        # Analyze risk factors and sentiment
        if utilization > warehouse_capacity_threshold or row['Risk Analysis'] == risk_threshold:
            if row['Sentiment'] == sentiment_threshold:
                alerts.append((row['Month'], "SELL", f"High utilization ({utilization:.2f}), {row['Risk Analysis']} risk, {row['Sentiment']} sentiment"))
            else:
                alerts.append((row['Month'], "MONITOR", f"High utilization ({utilization:.2f}) with {row['Risk Analysis']} risk"))
        elif utilization < 0.4:  # If utilization is very low
            alerts.append((row['Month'], "BUY", f"Low utilization ({utilization:.2f}), consider buying material"))

    return alerts

# Sample CSV data creation
data = {
    'Month': ['January', 'February', 'March'],
    'Warehouse Capacity': [10000, 10000, 10000],
    'Monthly Incoming': [8500, 6000, 3000],
    'Monthly Outgoing': [8000, 7000, 2500],
    'Risk Analysis': ['Medium', 'High', 'Low'],
    'Sentiment': ['Neutral', 'Negative', 'Positive']
}

# Save sample data to CSV for demonstration
sample_file = "warehouse_data.csv"
pd.DataFrame(data).to_csv(sample_file, index=False)

# Analyze the warehouse data
alerts = analyze_warehouse_data(sample_file)

# Display alerts
for alert in alerts:
    print(f"Month: {alert[0]}, Action: {alert[1]}, Reason: {alert[2]}")
