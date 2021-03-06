import React from 'react';
import { Button, Toolbar, ToolbarItem, ToolbarSpacer } from '@progress/kendo-react-buttons';
import { Window } from '@progress/kendo-react-dialogs';
import { connect } from 'react-redux';
import Camera from './Camera';
import {bindActionCreators} from "redux";
import cameraActions from "../actions/cameraActions";

export class CameraPlaceHolder extends React.Component{
    constructor(props){
        super(props);

        this.state = {
            hidden:false,
            cameraSource: JSON.parse(JSON.stringify(props.cameraSource)),
            previousCameraSource: "",
            cameraSourceWindowVisible: false,
            vidSrc: '#'
        }
        this.updateCameraSource = this.updateCameraSource.bind(this);
        this.toggleCameraSourceDialog = this.toggleCameraSourceDialog.bind(this);
        this.cancelCameraSourceUpdate = this.cancelCameraSourceUpdate.bind(this);
        this.viewCamera = this.viewCamera.bind(this);
        this.startCamera = this.startCamera.bind(this);
        this.stopCamera = this.stopCamera.bind(this);
    }
    startCamera(){
        this.props.camActions.startCamera();
    }
    stopCamera() {
        this.props.camActions.stopCamera();
    }
    toggleCameraSourceDialog(){

        if(!this.state.cameraSourceWindowVisible){
            this.setState({
            previousCameraSource: this.state.cameraSource});
        }
        this.setState({
            cameraSourceWindowVisible: !this.state.cameraSourceWindowVisible
        });
    }
    cancelCameraSourceUpdate() {
        this.setState({
            cameraSource: this.state.previousCameraSource,
            cameraSourceWindowVisible: false
        });
    }

    updateCameraSource(e){
        this.setState({
            cameraSource: e.target.value
        });
    }
    viewCamera(){
        this.props.camActions.viewCamera(!this.props.camView);
    }
    render() {
        return(<span>
                   <div className="camera-placeholder" hidden={this.props.camView}>
                       <div className="vertical-center">
                           <div>
                               <i className="fa fa-video-camera fa-5x"/>
                           </div>
                           <p>Camera</p>
                           <p style={{ color: this.props.status === false ? 'red' : 'green' }}>{this.props
                               .status === false ? 'Disconnected':'Connected'
                           }</p>
                           <Button onClick={this.viewCamera}>View Camera</Button>
                       </div>
                       <Camera hidden={!this.props.camView} vidSrc={this.state.vidSrc}/>
                   </div>
                   <Toolbar className="camera-placeholder-toolbar">
                       <ToolbarItem>
                           <div className="camera-placeholder-toolbar-icon">
                               <span className="k-icon k-i-play"/>
                           </div>
                       </ToolbarItem>
                       <ToolbarItem>
                           <p style={{ color: 'white', fontWeight: 'bold' }}>Video Source: <span style={{
                                color: this.props.cameraSource === '' ? 'red' : 'Green'
                            }}>{this.props.cameraSource === ''
                                ? 'No camera uri found.'
                                : this.props.cameraSource}</span></p>
                       </ToolbarItem>
                       <ToolbarSpacer/>
                       <ToolbarItem>
                            <Button onClick={this.startCamera} disabled={this.props.camStarted}>Start Camera</Button>
                            <Button onClick={this.stopCamera} disabled={!this.props.camStarted}>Stop Camera</Button>
                            
                       </ToolbarItem>
                   </Toolbar>
                   {this.state.cameraSourceWindowVisible &&
                       <Window title={"Camera Source"} onClick={this.toggleCameraSourceDialog}
                               initialTop={100}
                               initialLeft={100}
                               closeButton={""}
                               maximizeButton={""}
                               minimizeButton={""}>
                           <form className="k-form">
                               <fieldset>
                                   <legend>Set/Edit Camera Uri</legend>
                                   <label className="k-form-field">
                                       <span>URI</span>
                                       <input className="k-textbox" placeholder="rtsp://tygart.com/camera" onChange={
this.updateCameraSource} value={this.state.cameraSource}/>
                                   </label>
                               </fieldset>
                               <div className="text-right">
                                   <button type="button" className="k-button" onClick={this.cancelCameraSourceUpdate
}>Cancel</button>
                                   <button type="button" className="k-button" onClick={this.toggleCameraSourceDialog
}>Save &amp; Start</button>
                               </div>
                           </form>
                       </Window>
                   }
               </span>);
    }
}
const mapStateToProps = (state,ownProps)=> {
    let camUri = state.settings.settings.filter(s => s.name.toLowerCase() === "rtsp-url");
    let camStatus = state.status.statuses.filter(s => s.name.toLowerCase() === "statustype.stream");
    return{
        cameraSource: camUri.length > 0 ? camUri[0].setting : '',
        class: ownProps.className,
        status: camStatus.length > 0 ? (camStatus[0].status === 'true') : false,
        camStarted: state.camera.started,
        camView: state.camera.viewStarted
    }
}
const mapDispatchToActions = (dispatch)=>{
    return {
        camActions: bindActionCreators(cameraActions,dispatch)
    }
}
export default connect(mapStateToProps, mapDispatchToActions)(CameraPlaceHolder);
