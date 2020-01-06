import React from 'react';

// import {Button} from 'react-bootstrap'
import './pnls_list.css';
import io from 'socket.io-client';
import Tb from './totalpnl';


class TotalPnl extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }
 

  componentDidMount = (event) => {
    this.socket = io("http://192.168.0.103:5004");
    this.socket.on('total_pnl', (msg) => {
      const parsed = JSON.parse(msg)
      
      const sortData = parsed['data']
      
    //   const sortdata = sortData.sort((a, b) => a.algoName.localeCompare(b.algoName));

      
      this.setState({ data: sortData })
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
export default TotalPnl;