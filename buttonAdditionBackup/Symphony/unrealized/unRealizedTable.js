import React from 'react';
import Table from 'react-bootstrap/Table';
// import './Table.css';
import './unRealized.css';
const columns = ["Client ID" , "UnRealized Total"]
      
export default function Tb(props) {
    return (
        <div>
            <Table responsive striped bordered hover size='sm'>                
                <thead>
                    <tr>{
                        columns.map(col => (
                            <th id ="head">
                                {col}
                            </th>
                        ))
                    }
                    </tr>
                </thead>
                <tbody>
                    {
                        props.data.map(row => {
                            return(
                            <tr>
                                <td>
                                    {row.clientID}
                                </td>
                                <td>
                                    {row.unRealizedTotal}
                                </td>
                            </tr>
                        )
                    })
                    }
                </tbody>
            </Table>
        </div>
    );
}
