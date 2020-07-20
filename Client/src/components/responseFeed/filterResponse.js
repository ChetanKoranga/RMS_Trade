import React, { useState, useEffect } from "react";
import MUIDataTable from "mui-datatables";
import io from "socket.io-client";
import { Helmet } from "react-helmet";

const socket = io.connect("localhost:5013");

function App() {
  const columns = [
    "ClientID",
    "Time Stamp",
    "Algo",
    "Symbol",
    "Quantity",
    "Buy/Sell",
    "Order Status",
    "Order Average Traded Price",
    "Rejected Reason",
  ];

  const options = {
    filter: true,
    filterType: "dropdown",
    responsive: "vertical",
    tableBodyHeight: "500px",
  };

  const [state, setState] = useState([]);

  useEffect(() => {
    socket.on("filter_response_data", (res) => {
      try {
        // const parsed = JSON.parse(res);

        // console.log(result);
        setState(res);
        //
      } catch (error) {
        console.log("No Data Available");
      }
    });
  });

  return (
    <React.Fragment>
      <Helmet>
        <title>Filterable Response Table</title>
      </Helmet>
      <MUIDataTable
        title={"Response Feed "}
        data={state.map((item) => {
          return [
            item.clientID,
            item.time_stamp,
            item.algoname,
            item.symbol,
            item.quantity,
            item.buy_sell,
            item.orderStatus,
            item.OrderAverageTradedPrice,
            item.cancelrejectreason,
          ];
        })}
        columns={columns}
        options={options}
      />
    </React.Fragment>
  );
}

export default App;
