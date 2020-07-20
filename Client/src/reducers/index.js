import { combineReducers } from "redux";

const initialState = [];
// const initialClientTotalPnlState = []

const cumulativeReducer = (state = initialState, action) => {
  if (action.type === "INITIAL_DATA") return action.cumulativedata;
  return state;
};
const netpositionsReducer = (state = initialState, action) => {
  if (action.type === "NETPOSITIONS_DATA") return action.netpositionsdata;
  return state;
};

const responseReducer = (state = initialState, action) => {
  if (action.type === "RESPONSE_DATA") return action.responsedata;
  return state;
};

const clientOrdersReducer = (state = initialState, action) => {
  if (action.type === "CLIENTORDERS_DATA") return action.clientordersdata;
  return state;
};

const OptionsCallReducer = (state = initialState, action) => {
  if (action.type === "OPTIONS_CALL_DATA") return action.OptionsCallReducer;
  return state;
};

const OptionsPutReducer = (state = initialState, action) => {
  if (action.type === "OPTIONS_PUT_DATA") return action.OptionsPutReducer;
  return state;
};

const clientTotalPnLReducer = (state = initialState, action) => {
  if (action.type === "CLIENT_TOTAL_PNL") return action.clienttotalpnldata;
  return state;
};

const pnlReducer = (state = initialState, action) => {
  if (action.type === "PNL_DATA") return action.pnldata;
  return state;
};

const tradeStateReducer = (state = initialState, action) => {
  if (action.type === "TRADESTATE_DATA") return action.payload;
  return state;
};

const AlarmReducer = (state = initialState, action) => {
  if (action.type === "ALARM_DATA") return action.payload;
  return state;
};

const combined = combineReducers({
  CumulativeData: cumulativeReducer,
  NetPositionsData: netpositionsReducer,
  ResponseData: responseReducer,
  ClientOrdersFeedData: clientOrdersReducer,
  ClientTotalPnLData: clientTotalPnLReducer,
  PnlData: pnlReducer,
  TradeState: tradeStateReducer,
  OptionsCallData: OptionsCallReducer,
  OptionsPutData: OptionsPutReducer,
  AlarmData: AlarmReducer,
});

export default combined;
