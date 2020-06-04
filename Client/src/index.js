import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";

import App from "./components/cumulative/app";
import Client1 from "./components/cumulative/clientd1";
// import Client2 from "./components/cumulative/clientd2";
import Client3 from "./components/cumulative/clientd3";
import Client4 from "./components/cumulative/clientd4";
import Client5 from "./components/cumulative/clientd5";
import Client6 from "./components/cumulative/clientd6";
import Client7 from "./components/cumulative/clientd7";
import Client8 from "./components/cumulative/clientd8";
import Client9 from "./components/cumulative/clientd9";
import Client10 from "./components/cumulative/clientd10";
import Client11 from "./components/cumulative/clientd11";
import Client12 from "./components/cumulative/clientd12";
import Client13 from "./components/cumulative/clientd13";

import CNP from "./components/netClientPosition/clientnetpositions";
import CNP1 from "./components/netClientPosition/ncl1";
import CNP2 from "./components/netClientPosition/ncl2";
import CNP3 from "./components/netClientPosition/ncl3";
import CNP4 from "./components/netClientPosition/ncl4";
import CNP5 from "./components/netClientPosition/ncl5";
import CNP6 from "./components/netClientPosition/ncl6";
import CNP7 from "./components/netClientPosition/ncl7";
import CNP8 from "./components/netClientPosition/ncl8";
import CNP9 from "./components/netClientPosition/ncl9";
import CNP10 from "./components//netClientPosition/ncl10";
import CNP11 from "./components//netClientPosition/ncl11";
import CNP12 from "./components//netClientPosition/ncl12";

import ClientTotalPnl from "./components/totalpnl/clienttotalpnl";
import Pnl from "./components/totalpnl/pnl";

import ResponseLog from "./components/responseFeed/response";
import ClientOrdersLog from "./components/clientOrders/cleintlog";

import OptionCall from "./components/options/optionCall";
import OptionPut from "./components/options/optionPut";

import Tradestatetoggler from "./components/tradestatetoggler/tradestatetoggler";
import Cl1 from "./components/tradestatetoggler/cl1";
import Cl3 from "./components/tradestatetoggler/cl3";
import Cl4 from "./components/tradestatetoggler/cl4";
import Cl5 from "./components/tradestatetoggler/cl5";
import Cl6 from "./components/tradestatetoggler/cl6";
import Cl7 from "./components/tradestatetoggler/cl7";
import Cl8 from "./components/tradestatetoggler/cl8";
import Cl9 from "./components/tradestatetoggler/cl9";
import Cl10 from "./components/tradestatetoggler/cl10";
import Cl11 from "./components/tradestatetoggler/cl11";
import Cl12 from "./components/tradestatetoggler/cl12";
import Cl13 from "./components/tradestatetoggler/cl13";

import appt from "./components/forms/appt";
import ManualOrderUpdater from "./components/forms/ManualOrderUpdater";
import Squareoff from "./components/forms/Squareoff";

import Monitor from "./components/monitor/monitor";

import reducers from "./reducers";
import thunk from "redux-thunk";
import { BrowserRouter as Router, Route } from "react-router-dom";

let store = createStore(reducers, applyMiddleware(thunk));

ReactDOM.render(
  <Provider store={store}>
    <Router>
      <Route path="/" exact component={App} />
      <Route path="/d7730001" component={Client1} />
      <Route path="/d7730003" component={Client3} />
      <Route path="/d7730004" component={Client4} />
      <Route path="/d7730005" component={Client5} />
      <Route path="/d7730006" component={Client6} />
      <Route path="/d7730007" component={Client7} />
      <Route path="/V7410004" component={Client8} />
      <Route path="/d18138" component={Client9} />
      <Route path="/d7730008" component={Client10} />
      <Route path="/d7730009" component={Client11} />
      <Route path="/d8460002" component={Client12} />
      <Route path="/d8460003" component={Client13} />

      <Route path="/clientnetposition" exact component={CNP} />
      <Route path="/clientnetposition/d18138" component={CNP1} />
      <Route path="/clientnetposition/d7730001" component={CNP2} />
      <Route path="/clientnetposition/d7730003" component={CNP3} />
      <Route path="/clientnetposition/d7730004" component={CNP4} />
      <Route path="/clientnetposition/d7730005" component={CNP5} />
      <Route path="/clientnetposition/d7730006" component={CNP6} />
      <Route path="/clientnetposition/d7730007" component={CNP7} />
      <Route path="/clientnetposition/d7730008" component={CNP8} />
      <Route path="/clientnetposition/d7730009" component={CNP9} />
      <Route path="/clientnetposition/d8460002" component={CNP10} />
      <Route path="/clientnetposition/d8460003" component={CNP11} />
      <Route path="/clientnetposition/V7410004" component={CNP12} />

      <Route path="/responselog" component={ResponseLog} />
      <Route path="/algosignalfeed" component={ClientOrdersLog} />

      <Route path="/clienttotalpnl" component={ClientTotalPnl} />
      <Route path="/pnl" component={Pnl} />

      <Route path="/tradestatetoggler" component={Tradestatetoggler} />
      <Route path="/d7730001status" component={Cl1} />
      <Route path="/d7730003status" component={Cl3} />
      <Route path="/d7730004status" component={Cl4} />
      <Route path="/d7730005status" component={Cl5} />
      <Route path="/d7730006status" component={Cl6} />
      <Route path="/d7730007status" component={Cl7} />
      <Route path="/V7410004status" component={Cl8} />
      <Route path="/d18138status" component={Cl9} />
      <Route path="/d7730008status" component={Cl10} />
      <Route path="/d7730009status" component={Cl11} />
      <Route path="/d8460002status" component={Cl12} />
      <Route path="/d8460003status" component={Cl13} />

      <Route path="/forms" component={appt} />
      <Route path="/orderupdater" component={ManualOrderUpdater} />
      <Route path="/squareoff" component={Squareoff}/>

      <Route path="/optionscall" component={OptionCall} />
      <Route path="/optionsput" component={OptionPut} />

      <Route path="/monitor" component={Monitor} />
    </Router>
  </Provider>,
  document.getElementById("root")
);
