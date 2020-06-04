import React from "react";
import { connect } from "react-redux";
import {
  ClientTotalPnlData,
  loadClientTotalPnlDataSocket
} from "../../actions";
import io from "socket.io-client";
import { Link } from "react-router-dom";

import { Menu, Sticky, Breadcrumb } from "semantic-ui-react";

let columns = ["Client ID", "Net PnL"];
let pnl_flag;
let socket;

const MapStateToProps = state => {
  const sortedstate = state.ClientTotalPnLData;
  console.log(state);
  const sorted = {
    data: sortedstate.sort((a, b) => a.clientID.localeCompare(b.clientID))
  };
  return sorted;
};

class ClientTotalPnl extends React.Component {
  constructor(props) {
    super(props);
    const { dispatch } = this.props;
    //    console.log(dispatch)
    // console.log(this.props)
    // socket = io.connect("http://192.168.1.6:5002")
    socket = io.connect("http://192.168.0.103:5008");
    dispatch(loadClientTotalPnlDataSocket(socket));
    socket.on("unRealized_data", res => {
      dispatch(ClientTotalPnlData(res));
    });
  }

  componentWillUnmount() {
    socket.disconnect();
    console.log("Socket Disconnected");
  }

  render() {
    // console.log(this.props.data)
    return (
      <div>
        <Sticky>
          <Menu style={{ margin: 0 }}>
            <Link to="/pnl">
              <Menu.Item>Clientwise Strategywise Live PnL</Menu.Item>
            </Link>
            <Link to="/clienttotalpnl">
              <Menu.Item active={true}>Clientwise Net PnL</Menu.Item>
            </Link>
          </Menu>
          <Breadcrumb>
            <h2>Clientwise Net PnL</h2>
          </Breadcrumb>
        </Sticky>
        <table className="ui celled table">
          <thead>
            <tr>
              {columns.map(col => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {this.props.data.map(row => {
              if (row.unRealized_pnl > 0) pnl_flag = "positive";
              else if (row.unRealized_pnl === 0) pnl_flag = "";
              else pnl_flag = "negative";

              return (
                <tr key={row._id}>
                  <td>{row.clientID}</td>
                  <td className={pnl_flag}>{row.unRealized_pnl}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

export default connect(MapStateToProps)(ClientTotalPnl);
