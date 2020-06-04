import React from "react";
import { connect } from "react-redux";
import { loadPnlDataSocket, PnlData } from "../../actions";
import io from "socket.io-client";
import { Link } from "react-router-dom";

import { Menu, Sticky, Breadcrumb } from "semantic-ui-react";

let columns = ["clientID", "Algo", "PnL"];
let pnl_flag;
let socket;

const MapStateToProps = state => {
  const sortedstate = state.PnlData;
  console.log(state);
  const sorted = {
    data: sortedstate.sort((a, b) => a.clientID.localeCompare(b.clientID))
  };
  return sorted;
};

class Pnl extends React.Component {
  constructor(props) {
    super(props);
    const { dispatch } = this.props;
    //    console.log(dispatch)
    // console.log(this.props)
    // socket = io.connect("http://192.168.1.6:5002")
    socket = io.connect("http://192.168.0.103:5004");
    dispatch(loadPnlDataSocket(socket));

    socket.on("total_pnl", res => {
      dispatch(PnlData(res));
    });
  }

  componentWillUnmount() {
    socket.disconnect();
    console.log("Socket Disconnected");
  }

  render() {
    return (
      <div>
        <Sticky>
          <Menu style={{ margin: 0 }}>
            <Link to="/pnl">
              <Menu.Item active={true}>
                Clientwise Strategywise Live PnL
              </Menu.Item>
            </Link>
            <Link to="/clienttotalpnl">
              <Menu.Item>Clientwise Net PnL</Menu.Item>
            </Link>
          </Menu>
          <Breadcrumb>
            <h2>Clientwise Strategywise Live PnL</h2>
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
              if (row.strategywise_pnl > 0) pnl_flag = "positive";
              else if (row.strategywise_pnl === 0) pnl_flag = "";
              else pnl_flag = "negative";
              return (
                <tr key={row._id}>
                  <td>{row.clientID}</td>
                  <td>{row.algoname}</td>
                  <td className={pnl_flag}>{row.strategywise_pnl}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

export default connect(MapStateToProps)(Pnl);
