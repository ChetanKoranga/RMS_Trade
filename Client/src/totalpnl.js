import React from 'react';
import Table from 'react-bootstrap/Table';
// import './Table.css';
const columns = ["clientID","Algo","PnL"]

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
                <tbody >
                    {
                        props.data.map(row =>{
                         return(
                            <tr key={row.strategywise_pnl}>
                                <td>
                                    {row.clientID}
                                </td>
                                <td>
                                    {row.algoName}
                                </td>
                                <td>
                                    {row.strategywise_pnl}
                                </td>
                            </tr>
                        )})
                    }
                </tbody>
            </Table>
        </div>
    );
}