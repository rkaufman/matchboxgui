import { userConstants } from '../constants/userConstants';
import produce from 'immer';

let token = JSON.parse(localStorage.getItem('auth_token'));
let tokenExp = localStorage.getItem('token_exp');
const initialState = token && tokenExp < Date.now() ? { loggedIn: true, token, loggingIn: false, tokenExp } : {loggingIn: false};

export default function authentication(state = initialState, action) {
    console.log(action.type);
    switch (action.type) {
        case userConstants.LOGIN_REQUEST:
            return {
                loggingIn: true,
                user: action.user
            };
        case userConstants.LOGIN_SUCCESS:
            return produce(state,
                draft => {
                    draft.loggingIn = false;
                    draft.loggedIn = true;
                    draft.token = action.user.token.access_token;
                    draft.tokenExp = Date(action.user.exp);
                });
        case userConstants.LOGIN_FAILURE:
            return {};
        case userConstants.LOGOUT:
            return produce(state, draft => {
                draft.loggingIn = false;
                draft.loggedIn = false;
                draft.token = null;
                draft.exp = Date.now();
            });
        default:
            return state;
    }
}