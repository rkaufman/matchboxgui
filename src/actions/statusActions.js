import * as types from './actionTypes';
import { actions as toastrActions } from 'react-redux-toastr';
import statusService from "../services/statusService";

const getStatusesSuccess = (stats)=>{
    return {type: types.GET_STATUSES_SUCCESS, stats};
}

const getStatuses = ()=>{
    return (dispatch)=>{
        return statusService.getAll().then(s=>{
            dispatch(getStatusesSuccess(s));
        }).catch(e=>{
            toastrActions.add({
                type: 'error',
                message: 'Failed to get statuses.',
                title: 'Error'
            })
        });
    }
}

export const statusActions = {
    getStatuses
}

export default statusActions;
