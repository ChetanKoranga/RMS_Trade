import React from 'react';
import Table from 'react-bootstrap/Table';
import './responselog.css';
const columns = ["ClientID","Time Stamp","Algo","Symbol","Quantity","Buy/Sell","Order Status","Order Average Traded Price","Rejected Reason"]

export default function Tb(props) {
    return (
        <div>
            <Table responsive striped bordered hover variant="dark" size='sm'>                
                <thead>
                    <tr>
                    {
                        columns.map(col => (
                            <th>
                                {col}
                            </th>
                        ))
                    }
                    </tr>
                </thead>
                <tbody>
                    {
                        props.data.map(row => (
                            <tr>
                                <td>
                                    {row.clientID}
                                </td>
                                <td>
                                    {row.time_stamp}
                                </td>
                                <td>
                                    {row.algoname}
                                </td>
                                <td>
                                    {row.symbol}
                                    </td>
                                <td>
                                    {row.quantity}
                                </td>
                                <td>
                                    {row.buy_sell}
                                </td>
                                <td>
                                    {row.orderStatus}
                                </td>
                                <td>
                                    {row.OrderAverageTradedPrice}
                                </td>
                                <td>
                                    {row.cancelrejectreason}
                                </td>
                            </tr>
                        ))
                    }
                </tbody>
            </Table>
        </div>
    );
}
