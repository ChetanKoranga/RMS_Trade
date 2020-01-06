import React from 'react';
import Table from 'react-bootstrap/Table';
// import './Table.css';
const columns = ["Algo","Symbol","Quantity","Buy/Sell","Time Stamp"]

export default function Tb(props) {
    return (
        <div>
            <Table responsive striped bordered hover variant="dark" size='sm'>                
                <thead>
                    <tr>{
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
                        props.data.map(row => 
                            (<tr>
                                <td>
                                    {row.clientID}
                                </td>
                                <td>
                                    {row.algoName}
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
                                    {row.time_stamp}
                                </td>
                            </tr>
                        )
                        )
                    }
                </tbody>
            </Table>
        </div>
    );
}
