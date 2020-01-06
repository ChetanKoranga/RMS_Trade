import React from 'react';

// import {Button} from 'react-bootstrap'
import './pnls_list.css';
import io from 'socket.io-client';
import Tb from './responselog';

// const socket = io("http://127.0.0.1:5000");
//
// socket.on('connect', () => {
//   socket.send("I am back");
// })
// socket.on('message', (msg) => {
//   console.log(msg);
//   const received_msg = msg
// })

class ResponseLog extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: [] }
  }
  // myChangeHandler = (event) => {
  //   this.setState({symbol: event.target.value});
  // }
  //
  // myChangeHandler2 = (event) => {
  //   this.setState({pnl:event.target.value});
  // }

  componentDidMount = (event) => {
    // this.socket = io("http://192.168.1.6:5003");
    this.socket = io("http://192.168.43.188:5003");
    this.socket.on('response_data', (msg) => {
      const parsed = JSON.parse(msg)
      
      const sortData = parsed['data']
   

      const sortdata = sortData.sort((b, a) => a.time_stamp.split(':').join().localeCompare(b.time_stamp.split(':').join()));
      
      this.setState({ data: sortdata });
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
export default ResponseLog;