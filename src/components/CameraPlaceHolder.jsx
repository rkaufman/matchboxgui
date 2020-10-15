import React from 'react';
import { Button, Toolbar, ToolbarItem, ToolbarSpacer } from '@progress/kendo-react-buttons';
import { connect } from 'react-redux';

export class CameraPlaceHolder extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            hidden:false,
            cameraSource: ''
        }
    }
    render(){
        return(<span>
                    <div className="camera-placeholder" hidden={this.state.hidden}>
                        <div className="vertical-center">
                        <div>
                            <i className="fa fa-video-camera fa-5x"/>
                        </div>
                        <p>Camera</p>
                        <p style={{color:this.props.status == "Disconnected"?'red':'green'}}>{this.props.status}</p>
                        <Button >Connect Camera</Button>
                        </div>
                    </div>
                    <Toolbar className="camera-placeholder-toolbar">
                        <ToolbarItem>
                            <div className="camera-placeholder-toolbar-icon">
                                <span className="k-icon k-i-play"/>
                            </div>
                        </ToolbarItem>
                        <ToolbarItem>
                            <p style={{color: 'white', fontWeight: 'bold'}}>Video Source: <span style={{color: this.state.cameraSource == '' ? 'red' : 'white'}}>{this.state.cameraSource == '' ? 'Not Connected' : this.state.cameraSource}</span></p>
                        </ToolbarItem>
                        <ToolbarSpacer/>
                        <ToolbarItem>
                            <Button>Connect Camera</Button>
                        </ToolbarItem>
                    </Toolbar>
                </span>)
    }
}
const mapStateToProps = (state,ownProps)=>{
    return{
        class: ownProps.className
    }
}
export default connect(mapStateToProps)(CameraPlaceHolder);