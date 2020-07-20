import React from 'react';

// import {Button} from 'react-bootstrap'
import './unRealized.css';
import io from 'socket.io-client';
import Tb from './unRealizedTable';


class UnRealized extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }
 

  componentDidMount = (event) => {
    this.socket = io("http://192.168.1.81:5008");
    this.socket.on('unRealized_data', (msg) => {
      const parsed = JSON.parse(msg)
      
      const sortData = parsed['data']
      
      const sortdata = sortData.sort((a, b) => a.clientID.localeCompare(b.clientID));

      
      this.setState({ data: sortdata })
      console.log(this.state.data);
    })
  }
  render() {
    return (
      <div>
        <div className='container-fluid'>
          <div className="unRealized_table" >
            <Tb data={this.state.data} />
          </div>
        </div>
      </div>
    );
  }
}
export default UnRealized;
