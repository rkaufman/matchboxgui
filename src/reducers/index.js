import { combineReducers } from "redux";
import alert from './alertReducer';
import authentication from './authenticationReducer';
import register from './registerReducer';
import users from './usersReducer';
import {reducer as toastrReducer} from 'react-redux-toastr';
import { routerReducer } from "react-router-redux";

export default combineReducers({
    alert: alert,
    authentication: authentication,
    register: register,
    users: users,
    toastr: toastrReducer,
    routing: routerReducer
})