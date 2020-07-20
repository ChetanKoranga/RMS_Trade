import React from "react";
import { connect } from "react-redux";
import { loadResponseDataSocket, ResponseData } from "../../actions";
import io from "socket.io-client";
import { Sticky, Breadcrumb } from "semantic-ui-react";
import "./responsefeed.css";

let columns = [
  "ClientID",
  "Time Stamp",
  "Algo",
  "Symbol",
  "Quantity",
  "Buy/Sell",
  "Order Status",
  "Order Average Traded Price",
  "Rejected Reason",
];
let socket;
let buy_sell_flag;
let cancelrejectreason_flag;
let timestamp_flag;

var moment = require('moment');

const MapStateToProps = (state) => {
  console.log(state);
  let sortedstate = state.ResponseData;
  const sorted = {
    data: sortedstate.sort((a, b) => b.time_stamp.localeCompare(a.time_stamp)),
  };
  return sorted;
};

class Responsedata extends React.Component {
  constructor(props) {
    super(props);
    const { dispatch } = this.props;
    //    console.log(dispatch)
    // console.log(this.props)
    // socket = io.connect("http://192.168.1.6:5003")
    socket = io.connect("http://192.168.0.103:5003");
    dispatch(loadResponseDataSocket(socket));

    socket.on("response_data", (res) => {
      dispatch(ResponseData(res));
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
        <Sticky>
          <Breadcrumb>
            <h2>ORDER RESPONSE FEED</h2>
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
              if (row.buy_sell === "BUY") buy_sell_flag = "positive";
              else buy_sell_flag = "negative";

              if (row.cancelrejectreason !== "")
                cancelrejectreason_flag = "negative";
              else cancelrejectreason_flag = "";
              var time=moment().format("HH:mm:ss");
              var start = moment.utc(time, "HH:mm:ss");
              console.log(start)


              var dt = (row.time_stamp).slice(0,8);
              console.log(dt.slice(0,8));
              var end = moment.utc(dt, "HH:mm:ss");
              var d = moment.duration(start.diff(end));
              var s = moment.utc(+d).format('HHmmss');

              
             

              // console.log(s);
              if (s <= 100) timestamp_flag = "Yellowcell";
              else if (s > 100) timestamp_flag = "normal";

              return (
                <tr key={row._id} className={timestamp_flag} >
                  <td>{row.clientID}</td>
                  <td>{row.time_stamp}</td>
                  <td>{row.algoname}</td>
                  <td>{row.symbol}</td>
                  <td>{row.quantity}</td>
                  <td className={buy_sell_flag}>{row.buy_sell}</td>
                  <td>{row.orderStatus}</td>
                  <td>{row.OrderAverageTradedPrice}</td>
                  <td className={cancelrejectreason_flag}>
                    {row.cancelrejectreason}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

export default connect(MapStateToProps)(Responsedata);
