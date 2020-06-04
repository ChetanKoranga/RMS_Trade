import React, { Component} from "react";
import { Form, Button ,Select} from "semantic-ui-react";
import {ButtonToolbar} from 'react-bootstrap'
import { connect } from "react-redux";
import './style.css';
import AddModal from './AddModal';


const Clientid = [
    { key: "a", text: "All", value: "All" },
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

  

class Forms extends Component {
  constructor(props) {
    super(props);
    this.state = { Stratergyname: "", Clientid: "" ,showModal:false};
    this.render = this.render.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleStratergyChange=this.handleStratergyChange.bind(this);
    this.handleClientidChange=this.handleClientidChange.bind(this);
    this.sendAll=this.sendAll.bind(this);
    this.algos = [];
  

    this.getAlgoDatafromapi();
    
  }

  handleSubmit = (event) => {
    // event.preventDefault();
    const submission_data = this.state;

    console.log(submission_data);
    this.squareoffUpdate(submission_data);
  };
    
  
  squareoffUpdate = (submission_data) => {
    fetch("http://127.0.0.1:5000/updatesquareoff", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(submission_data),
    });
    console.log( submission_data);
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

  onClickalgo = (event) => {
    this.getAlgoDatafromapi();
  };


  handleStratergyChange = (event, { value }) => {
    this.setState({
      Stratergyname: value,
    });
    
  };

  handleClientidChange = (event, { value }) => {
    this.setState({
      Clientid: value,
    });

  };

  sendAll=(event)=>{
    var state = Object.assign(this.state, { Stratergyname: "All" , Clientid:"All"});
    this.setState(state)
    this.handleSubmit()
    this.setState({showModal:false})
  }
  
  toggle=()=>{
    this.setState({showModal:true})
  }
  

  render() {
    let closeModal=()=>this.setState({showModal:false})
    return (
      <div className="container" style={{paddingTop:100}}>
        <h1>AUTO SQUAREOFF</h1>

        <Form >

            <Form.Group widths="equal">
              <Form.Field
                
                control={Select}
                value={this.state.Stratergyname}
                name="Stratergyname"
                onChange={this.handleStratergyChange}
                options={this.algos}
                label={{
                  children: "Stratergyname",
                  htmlFor: "form-select-control-Stratergyname",
                }}
                placeholder="Enter Stratergy"
                search
                searchInput={{ id: "form-select-control-Stratergyname" }}
              />
              
               <Form.Field
               control={Select}
               value={this.state.Clientid}
               name="Clientid"
               onChange={this.handleClientidChange}
               options={Clientid}
               label={{
                 children: "Clientid",
                 htmlFor: "form-select-control-Clientid",
               }}
               placeholder="Client ID"
               search
               searchInput={{ id: "form-select-control-Clientid" }}
             />
                

            </Form.Group>
            <Form.Field>
              <Button color="blue" onClick={this.handleSubmit}>SquareOFF</Button>
            </Form.Field>

            <ButtonToolbar>
            <Button color="red" onClick={this.toggle}>SQUAREOFF ALL</Button>
            <AddModal
            show={this.state.showModal}
            onHide={closeModal}
            sendAll={this.sendAll}/>
            </ButtonToolbar>
            
            
        

    
              
            
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
  
  


