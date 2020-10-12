import * as types from "./actionTypes";

export const alertActions = {
    success,
    failure,
    clear
}

function success(message) {
    return { type: types.SUCCESS, message };
}
function failure(message) {
    return { type: types.FAILURE, message };
}
function clear() {
    return { type: types.CLEAR };
}