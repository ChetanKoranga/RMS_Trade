import React from "react";
import { connect } from "react-redux";
import { loadOptionsPutDataSocket, OptionsPutData } from "../../actions";
import io from "socket.io-client";
import { Menu, Sticky, Breadcrumb } from "semantic-ui-react";
import { Link } from "react-router-dom";

// let top_columns = ["Call", "Put"];
let columns = [
  "Strike",
  "Put IV",
  "Put Delta",
  "Put Theta",
  "Put Vega",
  "Put Gamma"
];
let socket;
// let buy_sell_flag;
// let cancelrejectreason_flag;

class Optionsdata extends React.Component {
  constructor(props) {
    super(props);
    const { dispatch } = this.props;
    //    console.log(dispatch)
    // console.log(this.props)
    // socket = io.connect("http://192.168.1.6:5003")
    socket = io.connect("http://192.168.43.188:5010");
    dispatch(loadOptionsPutDataSocket(socket));

    socket.on("Options_Put_Data", res => {
      dispatch(OptionsPutData(res));
    });
  }
  OptionsData;

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
              <Menu.Item>Call</Menu.Item>
            </Link>
            <Link to="/optionsput">
              <Menu.Item active={true}>Put</Menu.Item>
            </Link>
          </Menu>
          <Breadcrumb>
            <h2>Option Chain (PUT)</h2>
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
                  <td>{row.Put_IV}</td>
                  <td>{row.Put_Delta}</td>
                  <td>{row.Put_Theta}</td>
                  <td>{row.Put_Vega}</td>
                  <td>{row.Put_Gamma}</td>
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
  let sortedstate = { data: state.OptionsPutData };
  //   const sorted = {
  //     data: sortedstate.sort((a, b) => b.time_stamp.localeCompare(a.time_stamp))
  //   };
  return sortedstate;
};

export default connect(MapStateToProps)(Optionsdata);
