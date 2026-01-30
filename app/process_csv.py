# process_csv.py
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime


def analyze_trades(csv_path, user_id):
    df = pd.read_csv(csv_path)

    print("\n=== RAW CSV ===")
    print(df)
    print("================\n")

    required_columns = ["date", "asset", "type", "quantity", "price"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV must include {required_columns}")

    # Normalize
    df["type"] = df["type"].str.upper()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Asset tracking
    portfolio = {}
    total_pnl = 0.0
    sell_count = 0
    win_count = 0
    pnl_over_time = []

    for _, row in df.iterrows():
        asset = row["asset"]
        qty = row["quantity"]
        price = row["price"]

        if asset not in portfolio:
            portfolio[asset] = {
                "quantity": 0.0,
                "avg_price": 0.0
            }

        if row["type"] == "BUY":
            current_qty = portfolio[asset]["quantity"]
            current_avg = portfolio[asset]["avg_price"]

            new_qty = current_qty + qty
            if new_qty > 0:
                new_avg = (
                    (current_qty * current_avg) + (qty * price)
                ) / new_qty
            else:
                new_avg = 0

            portfolio[asset]["quantity"] = new_qty
            portfolio[asset]["avg_price"] = new_avg

        elif row["type"] == "SELL":
            sell_count += 1

            avg_price = portfolio[asset]["avg_price"]
            trade_pnl = qty * (price - avg_price)
            total_pnl += trade_pnl

            if trade_pnl > 0:
                win_count += 1

            portfolio[asset]["quantity"] -= qty

            print(
                f"SELL {asset} | Qty: {qty} | "
                f"Sell @ {price} | Avg @ {avg_price:.2f} | "
                f"PnL: {trade_pnl:.2f}"
            )

        pnl_over_time.append(total_pnl)

    win_rate = (win_count / sell_count * 100) if sell_count else 0

    print("\n=== SUMMARY ===")
    print(f"Total PnL: {total_pnl:.2f}")
    print(f"Sells: {sell_count}")
    print(f"Wins: {win_count}")
    print(f"Win Rate: {round(win_rate, 2)}%")
    print("================\n")

    # === Chart ===
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    chart_filename = f"user_{user_id}_{timestamp}.png"
    chart_path = os.path.join("app/static/charts", chart_filename)
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)

    plt.figure(figsize=(7, 4))
    plt.plot(df["date"], pnl_over_time, marker="o")
    plt.title("Cumulative PnL Over Time")
    plt.xlabel("Date")
    plt.ylabel("PnL ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return {
        "pnl": round(total_pnl, 2),
        "win_rate": round(win_rate, 2),
        "chart": f"charts/{chart_filename}"
    }

