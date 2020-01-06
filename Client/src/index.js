import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import './index.css';
// import Pnl from './pnl_form';
import ResponseLog from './responsedata';
import Pnlist from './pnls_list';
import TotalPnl from "./totalpnldata";
// import SimpleTable from './material';

import * as serviceWorker from './serviceWorker';
// import Pnlist from './pnls_list';
// import io from 'socket.io-client';
// import { createStore } from 'redux';
// import { Provider } from 'react-redux';

// const store = createStore(reducer);

const routing = (
    <Router>
        <div>
            <Switch>
                <Route path="/" exact component={Pnlist} />
                <Route path="/responselog" component={ResponseLog} />
                <Route path="/pnl" component={TotalPnl} />
            </Switch>
        </div>
    </Router>
)

// const socket = io("http://127.0.0.1:5000");

ReactDOM.render(routing, document.getElementById('root'));
// ReactDOM.render(<Pnlist />, document.getElementById('pnl_list'));
// ReactDOM.render(<Propdemo />, document.getElementById('prop_demo'))


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();