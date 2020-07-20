import React, { Component } from "react";
import { Form, Button, Select } from "semantic-ui-react";
import "./style.css";

class Otpform extends Component {
  constructor(props) {
    super(props);
    this.state = { Algoname: "", OTP: "" };
    this.change = this.change.bind(this);
    this.render = this.render.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.algos = [];

    this.getAlgoDatafromapi();
  }

  handleSubmit = (event) => {
    event.preventDefault();
    const submission_data = this.state;

    console.log(submission_data);
    this.OtpUpdate(submission_data);
  };

  change = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  OtpUpdate = (submission_data) => {
    fetch("http://127.0.0.1:5000/updateotpdb", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(submission_data),
    });
    console.log(submission_data);
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

  handleAlgoChange = (event, { value }) => {
    this.setState({
      Algoname: value,
    });
    console.log("trigered", this.state.Algoname);
  };

  onClickalgo = (event) => {
    this.getAlgoDatafromapi();
  };

  render() {
    return (
      <div className="o">
        <h2 class="ui red label" style={{ marginLeft: 490, fontSize: 20 }}>
          OTP
        </h2>
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
            <Form.Field>
              <label>OTP</label>
              <input
                name="OTP"
                placeholder="OneTimePassword"
                value={this.state.OTP}
                onChange={(e) => this.change(e)}
                label={{ children: "OTP" }}
              />
            </Form.Field>
          </Form.Group>
          <Form.Field>
            <Button color="blue">Submit</Button>
          </Form.Field>
        </Form>
      </div>
    );
  }
}

export default Otpform;
