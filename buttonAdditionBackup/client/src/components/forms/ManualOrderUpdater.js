import React, { Component } from "react";
import { Menu, Form, Select, Button, Input, Icon } from "semantic-ui-react";
import { connect } from "react-redux";
import "./style.css";
import { Link } from "react-router-dom";

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

const exchange_segment = [
  { key: "a", text: "NSECM", value: "NSECM" },
  { key: "b", text: "NSEFO", value: "NSEFO" },
  { key: "c", text: "NSECD", value: "NSECD" },
  { key: "d", text: "MCXFO", value: "MCXFO" },
];

class Forms extends Component {
  constructor(props) {
    super(props);
    this.state = {
      Algoname: "",
      ClientID: "",
      ExchangeSegment: "",
      Symbol: "",
      OrderSide: "",
      OrderQuantity: "",
      OrderAverageTradedPrice: "",
      buycolor:"grey",
      sellcolor:"grey"
    };
 
    this.handleClientChange = this.handleClientChange.bind(this);
    this.handleExchangeSegmentChange = this.handleExchangeSegmentChange.bind(this);
    this.handleAlgoChange= this.handleAlgoChange.bind(this);
    this.buy = this.buy.bind(this);
    this.sell = this.sell.bind(this);
    this.render = this.render.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.algos = [];
    this.getAlgoDatafromapi();
  }

  handleAlgoChange = (event, { value }) => {
    this.setState({
      Algoname: value,
    });
    console.log("trigered", this.state.Algoname);
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

  

  handleSubmit(event) {
    event.preventDefault();
    const submission_data = this.state;
    console.log(submission_data);
    this.orderUpdate(submission_data);
  }

  handleClientChange = (event, { value }) => {
    this.setState({
      ClientID: value,
    });
    console.log("Triggered", this.state.ClientID);
  };

  handleExchangeSegmentChange = (event, { value }) => {
    this.setState({
      ExchangeSegment: value,
    });
  };

  change = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  buy = (e) => {
    this.setState({
      sellcolor:"grey",
      buycolor:"green",
      OrderSide: "buy",
      
    });
  };

  sell = (e) => {
    this.setState({
      sellcolor:"red",
      buycolor:"grey",
      OrderSide: "sell",
    
    });
  };

  orderUpdate = (submission_data) => {
    fetch("http://127.0.0.1:5000/updatemanualorder", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(submission_data),
    });
    console.log("heyaaakomalu", submission_data);
  };

  render() {
    return (
      <div className="container">
        <Menu style={{ margin: 0 }}>
          <Link to="/forms">
            <Menu.Item>Start/Stop and OTP</Menu.Item>
          </Link>
          <Link to="/orderupdater">
            <Menu.Item active={true}>Manual Order Updater</Menu.Item>
          </Link>
        </Menu>
        <h1 className="ui blue label" style={{ marginLeft: 450 , fontSize:20}}>
          ORDER UPDATE
        </h1>
        <Form >
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
            value={this.state.exchange_segment}
            name="ExchangeSegment"
            onChange={this.handleExchangeSegmentChange}
            options={exchange_segment}
            label={{
              children: "Exchange Segment",
              htmlFor: "form-select-control-exchange_segment",
            }}
            placeholder="Exchange Segment"
            search
              searchInput={{ id: "form-select-control-exchange_segment" }}
          />

          <Form.Field
            control={Input}
            value={this.state.Symbol}
            name="Symbol"
            onChange={this.change}
            label={{
              children:
                "Symbol  eg.- Stocks:'COALINDIA',MCX:'CRUDEOIL-I',Futures:'TATAGLOBAL19OCTFUT',Options:'BANKNIFTY03OCT1926300PE')",
              htmlFor: "form-select-control-Symbol",
            }}
            placeholder="Enter Symbol"
            search
            searchInput={{ id: "form-select-control-Symbol" }}
          />
          <Form.Field>
            <Button.Group style={{ marginLeft: 450 }}>
              <Button  animated="vertical"  onClick={this.buy} color={this.state.buycolor} >
                <Button.Content hidden value="buy">
                  BUY
                </Button.Content>
                <Button.Content visible>
                  <Icon name="cart arrow down" />
                </Button.Content>
              </Button>
              <Button.Or />
              <Button  animated="vertical"  onClick={this.sell} color={this.state.sellcolor}>
                <Button.Content hidden value="sell">
                  SELL
                </Button.Content>
                <Button.Content visible>
                  <Icon name="upload" />
                </Button.Content>
              </Button>
            </Button.Group>
            
          </Form.Field>

          <Form.Field
            control={Input}
            value={this.state.OrderQuantity}
            name="OrderQuantity"
            onChange={this.change}
            label={{
              children: "OrderQuantity",
              htmlFor: "form-select-control-OrderQuantity",
            }}
            placeholder="Enter OrderQuantity"
            search
              searchInput={{ id: "form-select-control-OrderQuantity" }}
          />
          <Form.Field
            control={Input}
            value={this.state.OrderAverageTradedPrice}
            name="OrderAverageTradedPrice"
            onChange={this.change}
            label={{
              children: "OrderAverageTradedPrice",
              htmlFor: "form-select-control-OrderAverageTradedPrice",
            }}
            placeholder="Enter OrderAverageTradedPrice"
            search
              searchInput={{ id: "form-select-control-OrderAverageTradedPrice" }}
          />

          <Button style={{ marginLeft: 475 }} color="blue" onClick={this.handleSubmit}>
            UPDATE
          </Button>
        </Form>
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
