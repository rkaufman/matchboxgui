import React from 'react';
import { Button, Toolbar, ToolbarItem, ToolbarSpacer } from '@progress/kendo-react-buttons';
import { Window } from '@progress/kendo-react-dialogs';
import { connect } from 'react-redux';
import Camera from './Camera';

export class CameraPlaceHolder extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            hidden:false,
            cameraSource: '',
            previousCameraSource: "",
            cameraSourceWindowVisible: false
        }
        this.updateCameraSource = this.updateCameraSource.bind(this);
        this.toggleCameraSourceDialog = this.toggleCameraSourceDialog.bind(this);
        this.cancelCameraSourceUpdate = this.cancelCameraSourceUpdate.bind(this);
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
    render() {
        return(<span>
                   <div className="camera-placeholder" hidden={this.state.hidden}>
                       <div className="vertical-center">
                           <div>
                               <i className="fa fa-video-camera fa-5x"/>
                           </div>
                           <p>Camera</p>
                           <p style={{ color: this.props.status === false ? 'red' : 'green' }}>{this.props
                               .status === false ? 'Disconnected':'Connected'
                           }</p>
                           <Button >View Camera</Button>
                       </div>
                        <Camera hidden={!this.state.cameraSourceWindowVisible}/>
                   </div>
                   <Toolbar className="camera-placeholder-toolbar">
                       <ToolbarItem>
                           <div className="camera-placeholder-toolbar-icon">
                               <span className="k-icon k-i-play"/>
                           </div>
                       </ToolbarItem>
                       <ToolbarItem>
                           <p style={{ color: 'white', fontWeight: 'bold' }}>Video Source: <span style={{
                                color: this.state.cameraSource === '' ? 'red' : 'Green'
                            }}>{this.state.cameraSource === ''
                                ? 'No camera uri found.'
                                : this.state.cameraSource}</span></p>
                       </ToolbarItem>
                       <ToolbarSpacer/>
                       <ToolbarItem>
                           <Button onClick={this.toggleCameraSourceDialog}>Connect/Start Camera</Button>
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
this.updateCameraSource} value={this.props.cameraUri}/>
                                   </label>
                               </fieldset>
                               <div className="text-right">
                                   <button type="button" className="k-button" onClick={this.cancelCameraSourceUpdate
}>Cancel</button>
                                   <button type="button" className="k-button" onClick={this.toggleCameraSourceDialog
}>Submit</button>
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
        status: camStatus.length > 0 ? (camStatus[0].status === 'true') : false

}
}
export default connect(mapStateToProps)(CameraPlaceHolder);