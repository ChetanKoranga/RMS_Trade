import React, { Fragment } from "react";
import ReactDOM from "react-dom";
import { AllRoutes } from "./routes";

import DrawerLeft from "./components/layouts/drawer";

ReactDOM.render(
  <Fragment>
    <DrawerLeft />
  </Fragment>,
  document.getElementById("root")
);
