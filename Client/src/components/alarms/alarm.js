import React, { Fragment } from "react";
import { connect } from "react-redux";
import { AlarmData, loadAlarmDataSocket } from "../../actions";
import io from "socket.io-client";
import "./alarm.css";
import { Helmet } from "react-helmet";
var moment = require("moment");

let columns = ["Alarm ID", "File", "System", "Reason", "Time"];
let socket;
// let status;
// let buy_sell_flag;
// let cancelrejectreason_flag;
let timestamp_flag;
let fontcolor;

class TradeState extends React.Component {
  constructor(props) {
    super(props);

    socket = io.connect("http://192.168.0.103:5006");
    // socket = io.connect("http://192.168.43.179:5009");
    this.props.loadAlarmDataSocket(socket);

    socket.on("alarm_data", (res) => {
      this.props.AlarmData(res);
    });
  }

  // componentWillUnmount() {
  //     socket.disconnect()
  //     console.log('Socket Disconnected')
  // }

  render() {
    console.log(this.props);
    return (
      <div>
        <Helmet>
          <title>Alarms Sound Identification</title>
        </Helmet>

        <Fragment>
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
                var time = moment().format("HH:mm:ss");
                var start = moment.utc(time, "HH:mm:ss");
                console.log(start);

                var dt = row.time_stamp.slice(0, 8);
                console.log(dt.slice(0, 8));
                var end = moment.utc(dt, "HH:mm:ss");
                var d = moment.duration(start.diff(end));
                var s = moment.utc(+d).format("HHmmss");

                // console.log(s);
                if (s <= 100) {
                  timestamp_flag = "rowcolor";
                  fontcolor = "fontcolor";
                } else if (s > 100) {
                  timestamp_flag = "normal";
                  fontcolor = "";
                }

                if (row.Start_Stop !== "STOP")
                  return (
                    <tr className={timestamp_flag} key={row._id}>
                      <td className={fontcolor}>{row["alarm id"]}</td>
                      <td className={fontcolor}>{row["file name"]}</td>
                      <td className={fontcolor}>{row.system}</td>
                      <td className={fontcolor}>{row.reason}</td>
                      <td className={fontcolor}>{row.time_stamp}</td>
                    </tr>
                  );
                return null;
              })}
            </tbody>
          </table>
        </Fragment>
      </div>
    );
  }
}

const mapDispatchToProps = {
  AlarmData: AlarmData,
  loadAlarmDataSocket: loadAlarmDataSocket,
};

const MapStateToProps = (state) => {
  // console.log(state);
  let sortedstate = state.AlarmData;
  const sorted = {
    data: sortedstate.sort((a, b) =>
      b["time_stamp"].localeCompare(a["time_stamp"])
    ),
  };
  return sorted;
};

export default connect(MapStateToProps, mapDispatchToProps)(TradeState);
