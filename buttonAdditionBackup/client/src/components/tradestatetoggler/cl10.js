import React, { Fragment } from "react";
import { connect } from "react-redux";
import { Sticky, Breadcrumb, Menu, Button } from "semantic-ui-react";
import { Link } from "react-router-dom";
import AddModal from './AddModal';
// import App from "./app";

let columns = [
  "ClientID",
  "Algo",
  "STOPER",
  "Start/Stop Status",
  "LossLimit",
  "Quantity_Multiple",
  "Trade Limit Per Day",
  "Quantity Limit Per Trade",
  "Lot Size",
  "Slice Size",
  "Wait Time",
  "Trade Limit Per Second",
  "Max Value Of Symbol Check"
];

// let status;
// let socket;
// let buy_sell_flag;
// let cancelrejectreason_flag;

class TradeState extends React.Component {
  constructor(props) {
    super(props);
    this.state={
      showModal:false,
      algo:'',
      client:''
    }
    this.handlebutton = this.handlebutton.bind(this);
  }

  handlebutton = (algoname, clientid) => {
    fetch("http://127.0.0.1:5000/updatetable", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({ algoname: algoname, clientid: clientid }),
    });
    this.setState({showModal:false})
    console.log("heyaaakomalu", { algoname: algoname, clientid: clientid });
  };

  toggle=(algo,client)=>{
    this.setState({showModal:true,
      algoname:algo,
      clientid:client })
  }
  // componentWillUnmount() {
  //     socket.disconnect()
  //     console.log('Socket Disconnected')
  // }

  render() {
    let closeModal=()=>this.setState({showModal:false})
    // console.log(this.props)
    return (
      <div>
      <Fragment>
        <Sticky>
          <Menu style={{ margin: 0 }}>
            <a href="/tradestatetoggler">
              <Menu.Item>Clientwise Strategy Allocation Status</Menu.Item>
            </a>
            <Link to="/d18138status">
              <Menu.Item>D18138</Menu.Item>
            </Link>
            <Link to="/d7730001status">
              <Menu.Item>D7730001</Menu.Item>
            </Link>
            <Link to="/d7730003status">
              <Menu.Item>D7730003</Menu.Item>
            </Link>
            <Link to="/d7730004status">
              <Menu.Item>D7730004</Menu.Item>
            </Link>
            <Link to="/d7730005status">
              <Menu.Item>D7730005</Menu.Item>
            </Link>
            <Link to="/d7730006status">
              <Menu.Item>D7730006</Menu.Item>
            </Link>
            <Link to="/d7730007status">
              <Menu.Item>D7730007</Menu.Item>
            </Link>
            <Link to="/d7730008status">
              <Menu.Item active={true}>D7730008</Menu.Item>
            </Link>
            <Link to="/d7730009status">
              <Menu.Item>D7730009</Menu.Item>
            </Link>
            <Link to="/d8460002status">
              <Menu.Item>D8460002</Menu.Item>
            </Link>
            <Link to="/d8460003status">
              <Menu.Item>D8460003</Menu.Item>
            </Link>
            <Link to="/V7410004status">
              <Menu.Item>V7410004</Menu.Item>
            </Link>
            
          </Menu>
          <Breadcrumb>
            <h2>D7730008 Status</h2>
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
              // if (row.buy_sell === "BUY") buy_sell_flag = "positive";
              // else buy_sell_flag = "negative";

              // if (row.cancelrejectreason !== "")
              //   cancelrejectreason_flag = "negative";
              // else cancelrejectreason_flag = "";

              if (row.ClientID === "D7730008" && row.Start_Stop !== "STOP")
                return (
                  <tr key={row._id}>
                    <td>{row.ClientID}</td>
                    <td>{row.algoname}</td>
                    <td>
                      <Button color="red" onClick={()=>this.toggle(row.algoname,row.ClientID)}>STOP</Button>   
                      
                    </td>
                    <td>{row.Start_Stop}</td>
                    <td>{row.losslimit}</td>
                    <td>{row.quantity_multiple}</td>
                    <td>{row.TradeLimitPerDay}</td>
                    <td>{row.QuantityLimitPerTrade}</td>
                    <td>{row.lotSize}</td>
                    <td>{row.sliceSize}</td>
                    <td>{row.waitTime}</td>
                    <td>{row.tradeLimitPerSecond}</td>
                    <td>{row.maxvalueofsymbolcheck}</td>
                  </tr>
                );
              return null;
            })}
          </tbody>
        </table>
      </Fragment>
      <AddModal
      show={this.state.showModal}
      onHide={closeModal}
      sendAll={() => this.handlebutton(this.state.algoname,this.state.clientid)}
    />
    </div>
    );
  }
}

const MapStateToProps = (state) => {
  console.log(state);
  let sortedstate = state.TradeState;
  const sorted = {
    data: sortedstate.sort((a, b) => b.ClientID.localeCompare(a.ClientID)),
  };
  return sorted;
};

export default connect(MapStateToProps)(TradeState);
