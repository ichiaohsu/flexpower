import React from "react";

export default function Report(props) {
    const { data } = props
    if (!data || data.length === 0) {
        return null
    }

    return (
        <div className="report-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>Hour</th>
                        <th>Number of Trades</th>
                        <th>Total BUY [MW]</th>
                        <th>Total Sell [MW]</th>
                        <th>PnL [Eur]</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={index}>
                            <td>{row[0]}</td>
                            <td>{row[1]}</td>
                            <td>{row[2]}</td>
                            <td>{row[3]}</td>
                            <td>{row[4]}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}