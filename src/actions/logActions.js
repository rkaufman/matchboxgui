import * as types from './actionTypes';
import { actions as toastrActions } from 'react-redux-toastr';
import logService from '../services/logService';

const getLogsSuccess = (logs) => {
    return { type: types.GET_LOGS_SUCCESS, logs };
}

const getLogs = () => {
    return (dispatch) => {
        return logService.getAll().then(l => {
            dispatch(getLogsSuccess(l));
        }).catch(e => {
            toastrActions.add({
                type: 'error',
                message: 'Failed to get logs.',
                title: 'Error'
            });
        });
    }
}

export const logActions = {
    getLogs
}

export default logActions;