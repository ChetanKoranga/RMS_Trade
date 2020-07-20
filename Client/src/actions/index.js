export const initialItems = (res) => ({
  type: "INITIAL_DATA",
  cumulativedata: JSON.parse(res),
});

export const netpositonsData = (res) => ({
  type: "NETPOSITIONS_DATA",
  netpositionsdata: JSON.parse(res),
});

export const ResponseData = (res) => ({
  type: "RESPONSE_DATA",
  responsedata: JSON.parse(res),
});

export const ClientOrdersData = (res) => ({
  type: "CLIENTORDERS_DATA",
  clientordersdata: JSON.parse(res),
});

export const PnlData = (res) => ({
  type: "PNL_DATA",
  pnldata: JSON.parse(res),
});

export const ClientTotalPnlData = (res) => ({
  type: "CLIENT_TOTAL_PNL",
  clienttotalpnldata: JSON.parse(res),
});

export const TradeStateData = (res) => ({
  type: "TRADESTATE_DATA",
  payload: JSON.parse(res),
});

export const OptionsCallData = (res) => ({
  type: "OPTIONS_CALL_DATA",
  responsedata: JSON.parse(res),
});

export const OptionsPutData = (res) => ({
  type: "OPTIONS_PUT_DATA",
  responsedata: JSON.parse(res),
});

export const MonitorData = (res) => ({
  type: "MONITOR_DATA",
  payload: JSON.parse(res),
});

export const AlarmData = (res) => ({
  type: "ALARM_DATA",
  payload: JSON.parse(res),
});

export const loadInitialDataSocket = (socket) => {
  return (dispatch) => {
    // dispatch(clearAllItems())
    socket.on("cumulative_data", (res) => {
      dispatch(initialItems(res));
    });
  };
};

export const loadNetPositionsDataSocket = (socket) => {
  return (dispatch) => {
    // dispatch(clearAllItems())
    socket.on("netpositions_data", (res) => {
      dispatch(netpositonsData(res));
    });
  };
};

export const loadResponseDataSocket = (socket) => {
  return (dispatch) => {
    // dispatch(clearAllItems())
    socket.on("response_data", (res) => {
      dispatch(ResponseData(res));
    });
  };
};

export const loadClientOrdersDataSocket = (socket) => {
  return (dispatch) => {
    // dispatch(clearAllItems())
    socket.on("clientOrder_data", (res) => {
      dispatch(ClientOrdersData(res));
    });
  };
};

export const loadPnlDataSocket = (socket) => {
  return (dispatch) => {
    // dispatch(clearAllItems())
    socket.on("total_pnl", (res) => {
      dispatch(PnlData(res));
    });
  };
};

export const loadClientTotalPnlDataSocket = (socket) => {
  return (dispatch) => {
    // dispatch(clearAllItems())
    socket.on("unRealized_data", (res) => {
      dispatch(ClientTotalPnlData(res));
    });
  };
};

export const loadTradeStateDataSocket = (socket) => {
  return (dispatch) => {
    // dispatch(clearAllItems())
    socket.on("TradeStateToggler_data", (res) => {
      dispatch(TradeStateData(res));
    });
  };
};

export const loadOptionsCallDataSocket = (socket) => {
  return (dispatch) => {
    // dispatch(clearAllItems())
    socket.on("Options_Call_Data", (res) => {
      console.log(res);
      dispatch(OptionsCallData(res));
    });
  };
};

export const loadOptionsPutDataSocket = (socket) => {
  return (dispatch) => {
    // dispatch(clearAllItems())
    socket.on("Options_Put_Data", (res) => {
      console.log(res);
      dispatch(OptionsPutData(res));
    });
  };
};

export const loadMonitorDataSocket = (socket) => {
  return (dispatch) => {
    socket.on("monitor_data", (res) => {
      dispatch(MonitorData(res));
    });
  };
};

export const loadAlarmDataSocket = (socket) => {
  return (dispatch) => {
    socket.on("alarm_data", (res) => {
      dispatch(AlarmData(res));
    });
  };
};
