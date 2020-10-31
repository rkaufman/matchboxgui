import {cameraService} from "../services";
import * as types from "./actionTypes";
import {serviceBase} from "../services";

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
        return cameraService.startCamera().then(serviceBase.handleResponse)
            .then(()=>{
                dispatch(startCameraSuccess());
            });
    }
}
const stopCamera = ()=>{
    return (dispatch)=> {
        return cameraService.stopCamera()
            .then(serviceBase.handleResponse)
            .then(() => {
                dispatch(stopCameraSuccess());
            });
    };
}
const viewCamera = (view)=>{
    return (dispatch)=> {
        return cameraService.viewCamera(view)
            .then(serviceBase.handleResponse)
            .then(() => {
                if(view === true){
                    dispatch(viewCameraStartSuccess());
                } else{
                    dispatch(viewCameraStopSuccess());
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
