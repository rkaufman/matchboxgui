import * as types from "./actionTypes";
import userService from "../services/userService";

export const userActions = {
    logout,
    login,
    loadUsers,
    usernameBlank
};

function logout(user) {
    return { type: types.LOGOUT, user };
}
function loadUsersSuccess(users) {
    return { type: types.LOAD_USERS_SUCCESS, users };
}
function loadUsersFailure(e) {
    return { type: types.LOAD_USERS_FAILURE, errors: e };
}

function loadUsers() {
    return function(dispatch) {
        return userService.loadUsers().then(u => {
            dispatch(loadUsersSuccess(u));
        }).catch(e => { dispatch(loadUsersFailure(e)); });
    };
}
export function loginSuccess(user) {
    return { type: types.LOGIN_SUCCESS, user };
}
export function loginFailure(err) {
    return { type: types.LOGIN_FAILURE, errors: err };
}
function usernameBlank() {
    return { type: types.FIELD_VALUE_INVALID, error: "Username cannot be blank." };
}

export function login(user) {
    return function(dispatch) {
        return userService.login(user).then(u => {
            dispatch(loginSuccess(u));
        }).catch(err => {
            dispatch(loginFailure(err));
        });
    };
}