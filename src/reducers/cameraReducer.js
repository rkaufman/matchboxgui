import { produce } from 'immer';
import * as types from '../actions/actionTypes';

export const cameraReducer = (state={cameraStarted: false,
viewStarted: false, started: false}, action)=>{
    switch (action.type){
        case types.START_CAMERA_SUCCESS:
            return produce(state, draft =>{
                draft.started = true;
            });
        case types.STOP_CAMERA_SUCCESS:
            return produce(state, draft=>{
                draft.started = false;
            });
        case types.VIEW_CAMERA_STARTED:
            return produce(state, draft=>{
                draft.viewStarted = true;
            });
        case types.VIEW_CAMERA_STOPPED:
            return produce(state, draft=>{
                draft.viewStarted = false;
            });
        default:
            return state;
    }
}

export default cameraReducer;
