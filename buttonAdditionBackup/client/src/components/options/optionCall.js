import React from "react";
import { connect } from "react-redux";
import { loadOptionsCallDataSocket, OptionsCallData } from "../../actions";
import io from "socket.io-client";
import { Menu, Sticky, Breadcrumb } from "semantic-ui-react";
import { Link } from "react-router-dom";

// let top_columns = ["Call", "Put"];
let columns = [
  "Strike",
  "Call IV",
  "Call Delta",
  "Call Theta",
  "Call Vega",
  "Call Gamma"
];
let socket;
// let buy_sell_flag;
// let cancelrejectreason_flag;

class Optionscalldata extends React.Component {
  constructor(props) {
    super(props);
    const { dispatch } = this.props;
    //    console.log(dispatch)
    // console.log(this.props)
    // socket = io.connect("http://192.168.1.6:5003")
    socket = io.connect("http://192.168.43.188:5010");
    dispatch(loadOptionsCallDataSocket(socket));

    socket.on("Options_Call_Data", res => {
      dispatch(OptionsCallData(res));
    });
  }

  componentWillUnmount() {
    socket.disconnect();
    console.log("Socket Disconnected");
  }

  render() {
    // console.log(this.props)
    return (
      <div>
        <Sticky>
          <Menu style={{ margin: 0 }}>
            <Link to="/optionscall">
              <Menu.Item active={true}>Call</Menu.Item>
            </Link>
            <Link to="/optionsput">
              <Menu.Item>Put</Menu.Item>
            </Link>
          </Menu>
          <Breadcrumb>
            <h2>Option Chain (CALL)</h2>
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
              return (
                <tr key={row.StrikePrice}>
                  <td>{row.StrikePrice}</td>
                  <td>{row.Call_IV}</td>
                  <td>{row.Call_Delta}</td>
                  <td>{row.Call_Theta}</td>
                  <td>{row.Call_Vega}</td>
                  <td>{row.Call_Gamma}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

const MapStateToProps = state => {
  console.log(state);
  let sortedstate = { data: state.OptionsCallData };
  //   const sorted = {
  //     data: sortedstate.sort((a, b) => b.time_stamp.localeCompare(a.time_stamp))
  //   };
  return sortedstate;
};

export default connect(MapStateToProps)(Optionscalldata);
