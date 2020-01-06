import React from 'react';

// import {Button} from 'react-bootstrap'
import './pnls_list.css';
import io from 'socket.io-client';
import Tb from './Table.js';


class Pnlist extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }
 

  componentDidMount = (event) => {
    // this.socket = io("http://192.168.0.103:5002");
    this.socket = io("http://192.168.43.188:5002");
    this.socket.on('cumulative_data', (msg) => {
      const parsed = JSON.parse(msg)
      
      const sortData = parsed['data']
      
      const sortdata = sortData.sort((a, b) => a.algoName.localeCompare(b.algoName));

      
      this.setState({ data: sortdata })
      console.log(this.state.data);
    })
  }
  render() {
    return (
      <div>
        <div className='container-fluid'>
          <div className="pnl_table" >
            <Tb data={this.state.data} />
          </div>
        </div>
      </div>
    );
  }
}
export default Pnlist;