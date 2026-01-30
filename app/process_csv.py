import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def analyze_trades(csv_path, user_id):
    df = pd.read_csv(csv_path)
    
    # Basic checks
    required_columns = ["date", "asset", "type", "quantity", "price"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV must include {required_columns}")
    
    # Calculate PnL
    df['total'] = df['quantity'] * df['price']
    pnl = df[df['type']=='SELL']['total'].sum() - df[df['type']=='BUY']['total'].sum()
    
    # Win rate
    wins = len(df[df['type']=='SELL'][df['price'] > df['price'].mean()])
    total_trades = len(df)
    win_rate = wins / total_trades if total_trades else 0
    
    # Simple chart
    plt.figure(figsize=(6,4))
    df.groupby('date')['total'].sum().plot(kind='line', title='PnL over Time')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    chart_path = f"charts/user_{user_id}_{timestamp}.png"
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    plt.savefig(chart_path)
    plt.close()
    
    return {"pnl": pnl, "win_rate": win_rate, "chart": chart_path}
