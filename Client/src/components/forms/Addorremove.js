import React, { Component } from "react";
import { Form, Button } from "semantic-ui-react";

class Addremove extends Component {
  constructor(props) {
    super(props);
    this.state = { algolist: "", action: "" };

    this.change = this.change.bind(this);

    this.render = this.render.bind(this);

    this.handleSubmitadd = this.handleSubmitadd.bind(this);
    this.handleSubmitremove = this.handleSubmitremove.bind(this);
  }

  handleSubmitadd = (event) => {
    event.preventDefault();
    var state = Object.assign(this.state, { action: "add" });
    this.setState(state);
    // alert("An algo was added:  " + JSON.stringify(this.state))
    const listdata = this.state;

    // console.log(listdata)
    this.updateListdata(listdata);
  };

  handleSubmitremove(event) {
    event.preventDefault();
    var state = Object.assign(this.state, { action: "remove" });
    this.setState(state);
    // alert("An algo was removed:  " + JSON.stringify(this.state));
    const listdata = this.state;

    console.log(listdata);
    this.updateListdata(listdata);
  }

  change = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  updateListdata = (listdata) => {
    fetch("http://127.0.0.1:5000/listupdate", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(listdata),
    }).then(() => {
      this.props.onClickalgo();
    });
    console.log("hey", listdata);
  };

  render() {
    return (
      <div>
        <Form>
          <Form.Group widths="equal">
            <Form.Field>
              <h2 style={{ marginLeft: 420, fontSize: 20 }}>
                ALGO START STOP CONTROLLER
              </h2>
              <label>Add_Algo</label>
              <input
                name="algolist"
                placeholder="add_or_remove_algo"
                value={this.state.algolist}
                onChange={(e) => this.change(e)}
                label={{ children: "add_algo" }}
              />
            </Form.Field>
          </Form.Group>
          <Form.Group widths="equal">
            <Form.Field>
              <Button color="blue" onClick={this.handleSubmitadd}>
                Add
              </Button>
            </Form.Field>

            <Form.Field>
              <Button color="blue" onClick={this.handleSubmitremove}>
                remove
              </Button>
            </Form.Field>
          </Form.Group>
        </Form>
      </div>
    );
  }
}

export default Addremove;
