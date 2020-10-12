import { combineReducers } from "redux";
import alert from './alertReducer';
import authentication from './authenticationReducer';
import register from './registerReducer';
import users from './usersReducer';

export default combineReducers({
    alert: alert,
    authentication: authentication,
    register: register,
    users: users
})