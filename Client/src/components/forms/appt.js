import React, { Component } from "react";
//import Toggler from "./tradestatetoggler";
import Addremove from "./Addorremove";
import Otpform from "./Otpform";
import { Alert, ButtonToolbar } from "react-bootstrap";
import { Menu, Form, Select, Button } from "semantic-ui-react";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import "./style.css";
var moment = require("moment");

var time = moment().format("hh:mm:ss.SSSS");
let alertdata;

const Clientid = [
  { key: "a", text: "ALL", value: "All" },
  { key: "b", text: "D7730001", value: "D7730001" },
  { key: "c", text: "D7730002", value: "D7730002" },
  { key: "d", text: "D7730003", value: "D7730003" },
  { key: "e", text: "D7730004", value: "D7730004" },
  { key: "f", text: "D7730005", value: "D7730005" },
  { key: "g", text: "D7730006", value: "D7730006" },
  { key: "h", text: "D7730007", value: "D7730007" },
  { key: "i", text: "D7730008", value: "D7730008" },
  { key: "j", text: "D7730009", value: "D7730009" },
  { key: "k", text: "D18138", value: "D18138" },
  { key: "l", text: "V7410004", value: "V7410004" },
  { key: "m", text: "D8460002", value: "D8460002" },
  { key: "n", text: "D8460003", value: "D8460003" },
];

const toggle = [
  { key: "a", text: "START", value: "START" },
  { key: "b", text: "STOP", value: "STOP" },
];

class Forms extends Component {
  constructor(props) {
    super(props);
    this.state = {
      Algoname: "",
      ClientID: "",
      Status: "",
      losslimit: "",
      quantity_multiple: "",
      TradeLimitPerDay: "",
      QuantityLimitPerTrade: "",
      lotSize: "",
      sliceSize: "",
      waitTime: "",
      tradeLimitPerSecond: "",
      maxvalueofsymbolcheck: "",
      timestamp: time,
      visible: false,
    };
    // this.losslimit=React.createRef();
    this.handleAlgoChange = this.handleAlgoChange.bind(this);
    this.handleClientChange = this.handleClientChange.bind(this);
    this.handleStatusChange = this.handleStatusChange.bind(this);
    this.render = this.render.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleGet = this.handleGet.bind(this);
    this.algos = [];

    this.getAlgoDatafromapi();
  }

  handleSubmit(event) {
    event.preventDefault();
    // alert("An essay was submitted:  " + JSON.stringify(this.state));

    const submission_data = this.state;

    console.log(submission_data);
    this.tradestatetogglerUpdate(submission_data);
  }

  handleGet(event) {
    event.preventDefault();
    const getdata = this.state;

    console.log(getdata);
    this.fetcherUpdate(getdata);
  }

  handleAlgoChange = (event, { value }) => {
    this.setState({
      Algoname: value,
    });
    console.log("trigered", this.state.Algoname);
  };

  handleClientChange = (event, { value }) => {
    this.setState({
      ClientID: value,
    });
    console.log("Triggered", this.state.ClientID);
  };

  handleStatusChange = (event, { value }) => {
    this.setState({
      Status: value,
    });
  };

  change = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  tradestatetogglerUpdate = async (submission_data) => {
    const res = await fetch("http://127.0.0.1:5000/updatedb", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(submission_data),
    });
    const response = await res.json();
    console.log(response);
    if (response.status === 200) {
      delete response.data._id;
      alertdata = JSON.stringify(response.data);
      // console.log(typeof alertdata);
      this.onShowAlert();
      console.log("success");
    }
    console.log("heyaaakomalu", submission_data);
  };

  fetcherUpdate = async (getdata) => {
    const res = await fetch("http://127.0.0.1:5000/frontendtobackend", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(getdata),
    });

    const data = await res.json();
    console.log(data);
    if (data.status === 200) {
      this.setState({
        losslimit: data.data.losslimit,
        quantity_multiple: data.data.quantity_multiple,
        TradeLimitPerDay: data.data.TradeLimitPerDay,
        QuantityLimitPerTrade: data.data.QuantityLimitPerTrade,
        lotSize: data.data.lotSize,
        sliceSize: data.data.sliceSize,
        waitTime: data.data.waitTime,
        tradeLimitPerSecond: data.data.tradeLimitPerSecond,
        maxvalueofsymbolcheck: data.data.maxvalueofsymbolcheck,
      });
    }
  };

  onShowAlert = () => {
    this.setState({ visible: true }, () => {
      window.setTimeout(() => {
        this.setState({ visible: false });
      }, 10000);
    });
  };

  getAlgoDatafromapi = async () => {
    while (this.algos.length > 0) {
      this.algos.pop();
    }
    const res = await fetch("http://127.0.0.1:5000/getalgo");
    const data = await res.json();
    for (const d of data) {
      const f = {
        key: d._id,
        value: d.value,
        text: d.text,
      };
      this.algos.push(f);
    }
  };

  onClickalgo = (event) => {
    this.getAlgoDatafromapi();
  };

  render() {
    return (
      <div className="container">
        <Menu style={{ margin: 0 }}>
          <Link to="/forms">
            <Menu.Item active={true}>Start/Stop and OTP</Menu.Item>
          </Link>
          <Link to="/orderupdater">
            <Menu.Item>Manual Order Updater</Menu.Item>
          </Link>
        </Menu>

        <Addremove onClickalgo={this.onClickalgo} />

        <Form>
          <Form.Group widths="equal">
            <Form.Field
              control={Select}
              value={this.state.AlgoName}
              name="Algoname"
              onChange={this.handleAlgoChange}
              options={this.algos}
              label={{
                children: "Algoname",
                htmlFor: "form-select-control-algoname",
              }}
              placeholder="Enter Algoname"
              search
              searchInput={{ id: "form-select-control-algoname" }}
            />
            <Form.Field
              control={Select}
              value={this.state.Clientid}
              name="ClientID"
              onChange={this.handleClientChange}
              options={Clientid}
              label={{
                children: "ClientID",
                htmlFor: "form-select-control-client",
              }}
              placeholder="Enter ClientID"
              search
              searchInput={{ id: "form-select-control-client" }}
            />
            <Form.Field
              control={Select}
              value={this.state.toggle}
              name="Status"
              onChange={this.handleStatusChange}
              options={toggle}
              label={{
                children: "Start/Stop",
                htmlFor: "form-select-control-toggle",
              }}
              placeholder="Start/Stop"
              search
              searchInput={{ id: "form-select-control-toggle" }}
            />
          </Form.Group>
          <Form.Group widths="equal">
            <Form.Field>
              <label>LossLimit</label>
              <input
                name="losslimit"
                placeholder="losslimit"
                type="text"
                value={this.state.losslimit}
                // ref={this.losslimit}
                onChange={(e) => this.change(e)}
                label={{ children: "loss_limit" }}
              />
            </Form.Field>
            <Form.Field>
              <label>Quantity_Multiple</label>
              <input
                name="quantity_multiple"
                placeholder="quantity_multiple"
                value={this.state.quantity_multiple}
                onChange={(e) => this.change(e)}
                label={{ children: "quantity_multiple" }}
              />
            </Form.Field>
            <Form.Field>
              <label>TradeLimitPerDay</label>
              <input
                name="TradeLimitPerDay"
                placeholder="TradeLimitPerDay"
                value={this.state.TradeLimitPerDay}
                onChange={(e) => this.change(e)}
                label={{ children: "TradeLimitPerDay" }}
              />
            </Form.Field>
            <Form.Field>
              <label>QuantityLimitPerTrade</label>
              <input
                name="QuantityLimitPerTrade"
                placeholder="QuantityLimitPerTrade"
                value={this.state.QuantityLimitPerTrade}
                onChange={(e) => this.change(e)}
                label={{ children: "QuantityLimitPerTrade" }}
              />
            </Form.Field>
          </Form.Group>
          <Form.Group widths="equal">
            <Form.Field>
              <label>lotSize</label>
              <input
                name="lotSize"
                placeholder="lotSize"
                value={this.state.lotSize}
                onChange={(e) => this.change(e)}
                label={{ children: "lotSize" }}
              />
            </Form.Field>
            <Form.Field>
              <label>sliceSize</label>
              <input
                name="sliceSize"
                placeholder="sliceSize"
                value={this.state.sliceSize}
                onChange={(e) => this.change(e)}
                label={{ children: "sliceSize" }}
              />
            </Form.Field>
            <Form.Field>
              <label>waitTime</label>
              <input
                name="waitTime"
                placeholder="waitTime"
                value={this.state.waitTime}
                onChange={(e) => this.change(e)}
                label={{ children: "waitTime" }}
              />
            </Form.Field>
            <Form.Field>
              <label>tradeLimitPerSecond</label>
              <input
                name="tradeLimitPerSecond"
                placeholder="tradeLimitPerSecond"
                value={this.state.tradeLimitPerSecond}
                onChange={(e) => this.change(e)}
                label={{ children: "tradeLimitPerSecond" }}
              />
            </Form.Field>
            <Form.Field>
              <label>Max Value Of Symbol Check</label>
              <input
                name="maxvalueofsymbolcheck"
                placeholder="max value of symbol check"
                value={this.state.maxvalueofsymbolcheck}
                onChange={(e) => this.change(e)}
                label={{ children: "maxvalueofsymbolcheck" }}
              />
            </Form.Field>
          </Form.Group>

          <Form.Group>
            <ButtonToolbar>
              <Button color="blue" onClick={this.handleSubmit}>
                Submit
              </Button>
              <div className="container">
                <Alert
                  variant="warning"
                  show={this.state.visible}
                  style={{
                    flexWrap: "wrap",
                    textAlign: "centre",
                    wordWrap: "break-word",
                  }}
                >
                  Submitted sucessfully:{alertdata}
                </Alert>
              </div>
            </ButtonToolbar>
          </Form.Group>
          <Button color="yellow" onClick={this.handleGet}>
            Get Values
          </Button>
        </Form>
        <Otpform onClickalgo={this.onClickalgo} />
      </div>
    );
  }
}

const MapStateToProps = (state) => {
  console.log(state);
  let sorted = state.Forms;

  return sorted;
};

export default connect(MapStateToProps)(Forms);
