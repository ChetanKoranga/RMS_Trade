import React, {Component} from 'react';
import {Modal,Button} from 'react-bootstrap';

class AddModal extends Component{
    

    render(){
        return (
            <Modal
              {...this.props}
              size="lg"
              aria-labelledby="contained-modal-title-vcenter"
              centered
            >
              <Modal.Body>
                <div className="container">
                    Are you Sure?
                </div>

                  
              </Modal.Body>
              <Modal.Footer>
                <Button variant="primary" onClick={this.props.sendAll}>Confirm</Button>
                <Button variant="danger" onClick={this.props.onHide}>Close</Button>
              </Modal.Footer>
            </Modal>
          );
    }
}

export default AddModal