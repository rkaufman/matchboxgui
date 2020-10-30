import { combineReducers } from "redux";
import alert from './alertReducer';
import authentication from './authenticationReducer';
import register from './registerReducer';
import users from './usersReducer';
import settings from './settingsReducer';
import {reducer as toastrReducer} from 'react-redux-toastr';
import { routerReducer } from "react-router-redux";
import statusReducer from "./statusReducer";
import logReducer from "./logReducer";

export default combineReducers({
    alert: alert,
    authentication: authentication,
    register: register,
    users: users,
    settings: settings,
    toastr: toastrReducer,
    routing: routerReducer,
    status: statusReducer,
    log: logReducer
})
