import React from "react";
import { connect } from "react-redux";
import { loadInitialDataSocket, initialItems } from "../../actions";
import io from "socket.io-client";
import { Link } from "react-router-dom";

import { Menu, Sticky, Breadcrumb } from "semantic-ui-react";
import { Helmet } from "react-helmet";

let columns = [
  "Client ID",
  "Algo",
  "Symbol",
  "Quantity",
  "Buy/Sell",
  "Time Stamp",
];
let socket;
let buy_sell_flag;
let quantity_flag;

class CumulativeData extends React.Component {
  constructor(props) {
    super(props);

    //    console.log(dispatch)
    // console.log(this.props)
    // socket = io.connect("http://192.168.1.6:5002")
    socket = io.connect("http://192.168.0.103:5002");
    this.props.loadInitialDataSocket(socket);

    socket.on("cumulative_data", (res) => {
      this.props.initialItems(res);
    });
  }

  render() {
    // console.log(this.props)
    return (
      <div>
        <Helmet>
          <title>Live Clientwise Strategy-Symbol-Quantity</title>
        </Helmet>
        <Sticky>
          <Menu style={{ margin: 0 }}>
            <a href="/">
              <Menu.Item active={true}>
                Live Clientwise Strategy-Symbol-Quantity
              </Menu.Item>
            </a>

            <Link to="/d18138">
              <Menu.Item>D18138</Menu.Item>
            </Link>
            <Link to="/d7730001">
              <Menu.Item>D7730001</Menu.Item>
            </Link>
            <Link to="/d7730003">
              <Menu.Item>D7730003</Menu.Item>
            </Link>
            <Link to="/d7730004">
              <Menu.Item>D7730004</Menu.Item>
            </Link>
            <Link to="/d7730005">
              <Menu.Item>D7730005</Menu.Item>
            </Link>
            <Link to="/d7730006">
              <Menu.Item>D7730006</Menu.Item>
            </Link>
            <Link to="/d7730007">
              <Menu.Item>D7730007</Menu.Item>
            </Link>
            <Link to="/d7730008">
              <Menu.Item>D7730008</Menu.Item>
            </Link>
            <Link to="/d7730009">
              <Menu.Item>D7730009</Menu.Item>
            </Link>
            <Link to="/d8460002">
              <Menu.Item>D8460002</Menu.Item>
            </Link>
            <Link to="/d8460003">
              <Menu.Item>D8460003</Menu.Item>
            </Link>
            <Link to="/V7410004">
              <Menu.Item>V7410004</Menu.Item>
            </Link>
          </Menu>
          <Breadcrumb>
            <h2>Live Clientwise Strategy-Symbol-Quantity</h2>
          </Breadcrumb>
        </Sticky>
        <table className="ui celled table">
          ``
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {this.props.data.map((row) => {
              if (row.quantity >= 0) {
                quantity_flag = "positive";
                if (row.buy_sell === "BUY") buy_sell_flag = "positive";
                else buy_sell_flag = "negative";
              } else {
                quantity_flag = "negative";
                if (row.buy_sell === "BUY") buy_sell_flag = "positive";
                else buy_sell_flag = "negative";
              }
              if (row.quantity !== 0) {
                return (
                  <tr key={row._id}>
                    <td>{row.clientID}</td>
                    <td>{row.algoName}</td>
                    <td>{row.symbol}</td>
                    <td className={quantity_flag}>{row.quantity}</td>
                    <td className={buy_sell_flag}>{row.buy_sell}</td>
                    <td>{row.time_stamp}</td>
                  </tr>
                );
              }
              return null;
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

const MapStateToProps = (state) => {
  console.log(state);
  let sortedstate = state.CumulativeData;
  const sorted = {
    data: sortedstate.sort((a, b) => a.algoName.localeCompare(b.algoName)),
  };
  return sorted;
};

const MapDispatchToProps = {
  loadInitialDataSocket: loadInitialDataSocket,
  initialItems: initialItems,
};

export default connect(MapStateToProps, MapDispatchToProps)(CumulativeData);
