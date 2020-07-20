import React from "react";
import io from "socket.io-client";
import { Sticky, Breadcrumb } from "semantic-ui-react";
import "./clientfeed.css";
import { ClientOrdersData, loadClientOrdersDataSocket } from "../../actions";
import { connect } from "react-redux";
import { Helmet } from "react-helmet";
let columns = [
  "ClientID",
  "Time Stamp",
  "Algo",
  "Symbol",
  "Quantity",
  "Product Type",
  "Buy/Sell",
  "Order Status",
];
let socket;
let buy_sell_flag;

let timestamp_flag;
var moment = require("moment");

class ClientOrdersFeed extends React.Component {
  constructor(props) {
    super(props);
    const { dispatch } = this.props;
    //    console.log(dispatch)
    // console.log(this.props)
    // socket = io.connect("http://192.168.1.6:5003")
    socket = io.connect("http://192.168.0.103:5007");
    dispatch(loadClientOrdersDataSocket(socket));

    socket.on("response_data", (res) => {
      dispatch(ClientOrdersData(res));
    });
  }

  // componentWillUnmount() {
  //     socket.disconnect()
  //     console.log('Socket Disconnected')
  // }

  render() {
    // console.log(this.props)
    return (
      <div>
        <Helmet>
          <title>Algo Signal Feed</title>
        </Helmet>
        <Sticky>
          <Breadcrumb>
            <h2>Algo Signal Feed</h2>
          </Breadcrumb>
        </Sticky>
        <table className="ui celled table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {this.props.data.map((row) => {
              // let currentHours = new Date().getHours();
              // let currentMinutes = new Date().getMinutes();
              if (row.orderside === "BUY") buy_sell_flag = "positive";
              else buy_sell_flag = "negative";

              var time = moment().format("HH:mm:ss");
              var start = moment.utc(time, "HH:mm:ss");
              console.log(start);

              var dt = row.timestamp.slice(0, 8);
              console.log(dt.slice(0, 8));
              var end = moment.utc(dt, "HH:mm:ss");
              var d = moment.duration(start.diff(end));
              var s = moment.utc(+d).format("HHmmss");

              // let timestamp_hour = parseInt(row.timestamp.toString());
              // let timestamp_minute = parseInt(
              //   row.timestamp.toString().slice(3, 5)
              // );
              // console.log(currentMinutes, timestamp_minute);

              if (s <= 100) timestamp_flag = "Bluecell";
              else if (s > 100) timestamp_flag = "normal";

              return (
                <tr key={row._id} className={timestamp_flag}>
                  <td>{row.clientID}</td>
                  <td>{row.timestamp}</td>
                  <td>{row.algoname}</td>
                  <td>{row.symbol}</td>
                  <td>{row.quantity}</td>
                  <td>{row.productType}</td>
                  <td className={buy_sell_flag}>{row.orderside}</td>
                  <td>{row.orderstatus}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

const MapStateToProps = (state) => {
  console.log(state);
  let sortedstate = state.ClientOrdersFeedData;
  const sorted = {
    data: sortedstate.sort((a, b) => b.timestamp.localeCompare(a.timestamp)),
  };
  return sorted;
};

export default connect(MapStateToProps)(ClientOrdersFeed);
