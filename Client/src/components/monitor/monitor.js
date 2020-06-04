import React from "react";
import { connect } from "react-redux";
import io from "socket.io-client";
import {
  loadMonitorDataSocket,
  MonitorData,
  //monitorStatusUpdate,
} from "../../actions";
import { Sticky, Breadcrumb, Form, Button } from "semantic-ui-react";
import "./monitor.css";

let columns = ["Algoname", "Time Stamp", "Status", "Trade", "Last Traded Time"];
let socket;
let buy_sell_flag;
let status_flag;
let timestamp_flag;
// console.log(Date.getTime())
// let cancelrejectreason_flag;

class MONITOR extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      algoName: "",
      Status: "STOP",
    };
    this.render = this.render.bind(this);
    this.onSubmit = this.onSubmit.bind(this);

    //    console.log(dispatch)
    // console.log(this.props)
    // socket = io.connect("http://192.168.1.6:5003")
    socket = io.connect("http://192.168.43.188:5007");
    this.props.loadMonitorDataSocket(socket);

    socket.on("monitor_data", (res) => {
      this.props.MonitorData(res);
    });
  }

  monitorStatusUpdate = (data) => {
    // axios
    //   .post("http://127.0.0.1:5000/monitorupdate", JSON.stringify( data))
    //   .catch((err) => console.log(err));

    fetch("http://127.0.0.1:5000/monitorupdate", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(data),
    });
    console.log("ACTION====", data);
  };

  // componentWillUnmount() {
  //     socket.disconnect()
  //     console.log('Socket Disconnected')
  // }

  change = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  onSubmit = (e) => {
    e.preventDefault();
    console.log(this.state);
    this.monitorStatusUpdate(this.state);
  };

  render() {
    // console.log(this.props)
    return (
      <div>
        <Sticky>
          <Breadcrumb>
            <h2>MONITOR</h2>
          </Breadcrumb>
        </Sticky>
        <div className="ui container">
          <Form onSubmit={this.onSubmit}>
            <Form.Group widths="equal">
              <Form.Field>
                <label>Algoname</label>
                <input
                  name="algoName"
                  placeholder="Algoname"
                  value={this.state.algoName}
                  onChange={(e) => this.change(e)}
                />
              </Form.Field>
              <Form.Field>
                <label>Status</label>
                <input
                  name="Status"
                  //placeholder="algoname"
                  value="STOP"
                  onChange={(e) => e.preventDefault()}
                  label={{
                    children: "Status",
                    //htmlFor: "form-select-control-algoname"
                  }}
                />
              </Form.Field>
            </Form.Group>
            <Form.Field
              id="form-button-control-public"
              control={Button}
              content="Close"
            />
          </Form>
        </div>

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
              let currentHours = new Date().getHours();
              let currentMinutes = new Date().getMinutes();
              if (row.Trade === "BUY") buy_sell_flag = "positive";
              else if (row.Trade === "SELL") buy_sell_flag = "negative";
              if (row.Status === "WARNING! algo is not working")
                status_flag = "negative";
              else if (row.Status === "Running") status_flag = "positive";
              if (!row.last_traded_time) timestamp_flag = "normal";
              else {
                let timestamp_hour = parseInt(row.last_traded_time);
                let timestamp_minute = parseInt(
                  row.last_traded_time.slice(3, 5)
                );

                //console.log(timestamp_hour)
                //console.log(timestamp_minute)
                if (
                  currentHours - timestamp_hour === 0 &&
                  Math.abs(currentMinutes - timestamp_minute) <= 1
                )
                  timestamp_flag = "Yellowcell";
                else if (
                  currentHours - timestamp_hour === 0 &&
                  Math.abs(currentMinutes - timestamp_minute) > 1
                )
                  timestamp_flag = "normal";
                else if (
                  currentHours - timestamp_hour !== 0 &&
                  Math.abs(currentMinutes - timestamp_minute) < 1
                )
                  timestamp_flag = "normal";
                else if (
                  currentHours - timestamp_hour !== 0 &&
                  Math.abs(currentMinutes - timestamp_minute) > 1
                )
                  timestamp_flag = "normal";
                // var time_stamp_milli=new moment(row.Time_Stamp,'HH:mm:ss.SSS')
                // console.log(time_stamp_milli)

                //   if (row.cancelrejectreason !== "")
                //     cancelrejectreason_flag = "negative";
                //   else cancelrejectreason_flag = ""
              }
              return (
                <tr key={row._id} className={timestamp_flag}>
                  <td>{row.Algoname}</td>
                  <td>{row.Time_Stamp}</td>
                  <td className={status_flag}>{row.Status}</td>
                  <td className={buy_sell_flag}>{row.Trade}</td>
                  <td>{row.last_traded_time}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

const mapDispatchToProps = {
  loadMonitorDataSocket: loadMonitorDataSocket,
  MonitorData: MonitorData,
  //monitorStatusUpdate: monitorStatusUpdate,
};

const MapStateToProps = (state) => {
  console.log(state);
  let sortedstate = state.Monitor;
  const sorted = {
    data: sortedstate.sort((a, b) => b.Status.localeCompare(a.Status)),
  };
  return sorted;
};

export default connect(MapStateToProps, mapDispatchToProps)(MONITOR);
//export default MONITOR
