import React from 'react';
import Table from 'react-bootstrap/Table';
import './Table.css'
import ReactTable from 'react-table'

const columns = [
	{ Header: "Name", accessor: 'name' },
  { Header: "EditableCell", Cell: props => <input type="text"/>}
]

export default function Tb(props) {
    return (
        <div>
            <Table responsive striped bordered hover variant="dark" size='sm'>
            data={props.data}
				columns={}
				manual={true}
				getTrProps={(state, rowInfo) => {     
					return {
						style: {
							background: 'red',
						}        
         }
      }}
                
                <thead>
                    <tr>
                        <th>Algo</th>
                        <th>Symbol</th>
                        <th>Quantity</th>
                        <th>Buy/Sell</th>
                        <th>Time Stamp</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        props.data.map(row => (
                            <tr>
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
                                    {row.time_stamp}
                                </td>
                            </tr>
                        ))
                    }
                </tbody>
            </Table>
        </div >

    );
}
