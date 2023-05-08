import requests
from datetime import datetime
from typing import List, Dict 
from tabulate import tabulate

import argparse

def get_trades(url: str) -> List[Dict[str, str|int]]: 
    """
    get_trades uses the url to retrieve trades from API
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("failed to get trades data")
    return response

def response_to_report(response: List[Dict[str, str|int]]) -> List[List[str|int]]:
    """
    response_to_report take the responded JSON, and parse it into report format
    """
    reports = [None for i in range(0, 24)]
    total = [0 for i in range(0,4)]

    for trade in response.json():
        hour = trade.get("delivery_hour")
        # the number of trades, the total quantity sold, the total quantity bought and finally the pnl value
        if reports[hour] is None:
            reports[hour] = [0 for i in range(0,4)]

        reports[hour][0] += 1
        total[0] += 1
        if (direction := trade.get("direction"))== "sell":
            reports[hour][1] += trade.get("quantity")
            reports[hour][3] += trade.get("price") * trade.get("quantity")

            total[1] += trade.get("quantity")
            total[3] += trade.get("price") * trade.get("quantity")
        elif direction == "buy":
            reports[hour][2] += trade.get("quantity")
            reports[hour][3] -= trade.get("price") * trade.get("quantity")

            total[2] += trade.get("quantity")
            total[3] -= trade.get("price") * trade.get("quantity")

    results = [ ["{} - {}".format(i,i+1)] + x for i, x in enumerate(reports) if x is not None]
    results.append(["Total"] + total)
    return results

def parse_url() -> str: 
    """
    parse_url get the arguments from command line, and format the query url against API.
    """
    parser = argparse.ArgumentParser(description="generate report")

    parser.add_argument("--api-url", dest="url", type=str, action="store", default="http://localhost:8000/trades", help="The trades API URL")
    parser.add_argument("--trader-id", dest="trader_id", type=str, action="store", required=True, help="Unique id of a trader")
    parser.add_argument("--delivery-day", dest="delivery_day", type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),  action="store", required=True, help="Day on which the energy has to be delivered in local time.")
    args = parser.parse_args()
    return "{}?trader_id={}&delivery_day={}".format(args.url, args.trader_id, args.delivery_day)

if __name__ == "__main__":

    response = get_trades(parse_url())

    reports = response_to_report(response)

    print(tabulate(reports, headers=["Hour","Number of Trades","Total BUY [MW]", "Total Sell [MW]", "PnL [Eur]"]))
