import React, { Component } from "react";
import Toggler from "./tradestatetoggler";
import Addremove from "./Addorremove";
import { Sticky, Breadcrumb, Form, Select, Button } from "semantic-ui-react";

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

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      Algoname: "",
      ClientID: "",
      Status: "",
      losslimit: "",
      quantity_multiple: "",
    };
    this.handleAlgoChange = this.handleAlgoChange.bind(this);
    this.handleClientChange = this.handleClientChange.bind(this);
    this.handleStatusChange = this.handleStatusChange.bind(this);
    this.render = this.render.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
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

  tradestatetogglerUpdate = (submission_data) => {
    fetch("http://127.0.0.1:5000/updatedb", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(submission_data),
    });
    console.log("heyaaakomalu", submission_data);
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
      <div>
        <Sticky>
          <Breadcrumb>
            <h2>START/STOP</h2>
          </Breadcrumb>
        </Sticky>
        <div className="container">
          <Addremove onClickalgo={this.onClickalgo} />

          <Form onSubmit={this.handleSubmit}>
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
                  value={this.state.losslimit}
                  onChange={(e) => this.change(e)}
                  label={{ children: "loss_limit" }}
                />
              </Form.Field>
              <Form.Field>
                <label>Quantity_Multiple</label>
                <input
                  name="quantity_multiple"
                  placeholder="quantity_multiple"
                  value={this.state.multiple_quantity}
                  onChange={(e) => this.change(e)}
                  label={{ children: "quantity_multiple" }}
                />
              </Form.Field>
            </Form.Group>

            <Form.Field
              id="form-button-control-public"
              control={Button}
              content="Submit"
            />
          </Form>
        </div>
        <Toggler />
      </div>
    );
  }
}

export default App;
