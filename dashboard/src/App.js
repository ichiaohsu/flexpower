import React, { useState } from "react";
import Form from "./components/Form";
import Report from "./components/Report";

var apiHost = process.env.REACT_APP_API_HOST

const getTrades = async (state) => {
  const {trader_id, delivery_day} = state;
  const response = await fetch(
    `${apiHost}/trades?trader_id=${trader_id}&delivery_day=${delivery_day}`
    )
  let data = await response.json()

  const reports = {};
  const total = [0, 0, 0, 0];
  let results = [];
  data.forEach(trade => {
    const hour = trade.delivery_hour;
    // the number of trades, the total quantity sold, the total quantity bought and finally the pnl value
    if (reports[hour] === undefined) {
        reports[hour] = [0, 0, 0, 0];
    }

    reports[hour][0]++;
    total[0]++;
    const direction = trade.direction;
    if (direction === "sell") {
        reports[hour][1] += trade.quantity;
        reports[hour][3] += trade.price * trade.quantity;

        total[1] += trade.quantity;
        total[3] += trade.price * trade.quantity;
    } else if (direction === "buy") {
        reports[hour][2] += trade.quantity;
        reports[hour][3] -= trade.price * trade.quantity;

        total[2] += trade.quantity;
        total[3] -= trade.price * trade.quantity;
    }
    results = Object.entries(reports)
    .filter(([_, x]) => x !== undefined)
    .map(([i, x]) => [` ${i} - ${parseInt(i)+1}`, ...x]);

    results.push(["Total", ...total]);
  });
  return results
}

function App(props) {
  const [state, setState] = useState({
    trader_id: "",
    delivery_day: "2023-02-28",
  })
  const [data, setData] = useState(null)

  function handleInput(evt) {
    const value = evt.target.value;
    setState({
      ...state,
      [evt.target.name]: value
    });
  }

  async function handleSubmit(evt) {
    evt.preventDefault();
    const report = await getTrades(state)
    setData(report)
  }
  
  return (
    <div className="dashboard">
      <h1>Trades Dashboard</h1>
      <Form 
        traderId={state.trader_id} 
        deliveryDate={state.delivery_day}
        handleChange={handleInput}
        handleSubmit={handleSubmit}
      />
      <Report data={data}/>
    </div>
  );
}

export default App;
