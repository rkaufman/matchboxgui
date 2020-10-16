import { userConstants } from '../constants/userConstants';
import produce from 'immer';

let token = JSON.parse(localStorage.getItem('auth_token'));
const initialState = token ? { loggedIn: true, token } : {};

export default function authentication(state = initialState, action) {
  console.log(action.type)
  switch (action.type) {
    case userConstants.LOGIN_REQUEST:
      return {
        loggingIn: true,
        user: action.user
      };
    case userConstants.LOGIN_SUCCESS:
      return produce(state, draft =>{
        draft.loggedIn = true;
        draft.token = action.user.access_token;
      })
    case userConstants.LOGIN_FAILURE:
      return {};
    case userConstants.LOGOUT:
      return produce(state, draft =>{
        draft.loggedIn = false;
        draft.token = null
      });
    default:
      return state
  }
}