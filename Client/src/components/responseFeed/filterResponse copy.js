import React, { Component } from "react";
import io from "socket.io-client";
import { Helmet } from "react-helmet";

const socket = io.connect("localhost:5013");

const $ = require("jquery");
$.DataTable = require("datatables.net");

const columns = [
  {
    title: "ClientID",
    width: 120,
    data: "clientID",
  },
  {
    title: "Time Stamp",
    width: 180,
    data: "time_stamp",
  },
  {
    title: "Algo",
    width: 180,
    data: "algoname",
  },
  {
    title: "Symbol",
    width: 180,
    data: "symbol",
  },
  {
    title: "Quantity",
    width: 180,
    data: "quantity",
  },
  {
    title: "Buy/Sell",
    width: 180,
    data: "buy_sell",
  },
  {
    title: "Order Status",
    width: 180,
    data: "orderStatus",
  },
  {
    title: "Order Average Traded Price",
    width: 180,
    data: "OrderAverageTradedPrice",
  },
  {
    title: "Rejected Reason",
    width: 180,
    data: "cancelrejectreason",
  },
];

export class filterResponse extends Component {
  constructor() {
    super();
    this.state = { data: {} };
  }
  componentDidMount() {
    socket.on("filter_response_data", (res) => {
      try {
        const parsed = JSON.parse(res)[0];
        this.setState({ data: parsed }, () => {
          console.log("Incoming Data...", this.state);
        });
        //
      } catch (error) {
        console.log("No Data Available");
      }
    });
    $(this.refs.main).DataTable({
      dom: '<"data-table-wrapper"t>',
      data: this.state.data,
      columns,
      ordering: false,
    });
  }

  componentWillUnmount() {
    $(".data-table-wrapper")
      .find("table")
      .DataTable()
      .destroy(true);
  }

  render() {
    //
    return (
      <div>
        <Helmet>
          <title>Filterable Response Table</title>
        </Helmet>
        <table ref="main" />
      </div>
    );
  }
}

export default filterResponse;
