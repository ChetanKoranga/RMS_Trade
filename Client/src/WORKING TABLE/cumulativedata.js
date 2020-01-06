import React from 'react';

// import {Button} from 'react-bootstrap'
// import './pnls_list.css';
import io from 'socket.io-client';
import Tb from './customtable';

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
  constructor(rowprops) {
    super(rowprops);
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
    this.socket = io("http://127.0.0.1:5002");
    this.socket.on('message', (msg) => {
      const parsed = JSON.parse(msg)
      
      const sortData = parsed['data']
    
      this.setState({ data: sortData })
      console.log(this.state.data)
      this.socket.emit('loop_event');
    })
  }
  render() {
    return (

      
      <div>
        {/* <div className='container-fluid'> */}
          <div className="pnl_table" >
            <Tb data={this.state.data} />
          </div>
        {/* </div> */}
      </div>
    );
  }
}
export default ResponseLog;