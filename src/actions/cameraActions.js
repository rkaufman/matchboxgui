import {cameraService} from "../services";
import * as types from "./actionTypes";
import { actions as toastrActions } from 'react-redux-toastr';

const startCameraSuccess = ()=>{
    return{type:types.START_CAMERA_SUCCESS};
}
const stopCameraSuccess = ()=>{
    return {type: types.STOP_CAMERA_SUCCESS};
}
const viewCameraStopSuccess = ()=>{
    return{type: types.VIEW_CAMERA_STOPPED}
}
const viewCameraStartSuccess = ()=>{
    return {type: types.VIEW_CAMERA_STARTED}
}

const startCamera = ()=>{
    return (dispatch)=>{
        return cameraService.startCamera()
            .then(r=>{
                if (r.ok) {
                    dispatch(startCameraSuccess());
                } else {
                    toastrActions.add({
                        type: 'error',
                        message: 'Failed to start camera',
                        title: 'Error'
                    });
                }
                
            });
    }
}
const stopCamera = ()=>{
    return (dispatch)=> {
        return cameraService.stopCamera()
            .then((r) => {
                if (r.ok) {
                    dispatch(stopCameraSuccess());
                }else {
                    toastrActions.add({
                        type: 'error',
                        message: 'Failed to stop camera',
                        title: 'Error'
                    });
                }
            });
    };
}
const viewCamera = (view)=>{
    return (dispatch)=> {
        return cameraService.viewCamera(view)
            .then((r) => {
                if (r.ok) {
                    if (view === true) {
                        dispatch(viewCameraStartSuccess());
                    } else {
                        dispatch(viewCameraStopSuccess());
                    }
                } else {
                    toastrActions.add({
                        type: 'error',
                        message: 'Failed to start/stop camera view',
                        title: 'Error'
                    });
                }
            });
    }
}
const cameraActions = {
    startCameraSuccess,
    startCamera,
    stopCamera,
    viewCamera
};
export default cameraActions;
