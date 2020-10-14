import { userConstants } from '../constants/userConstants';

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
      return Object.assign(state,{
        loggedIn: true,
        user: action.user
      });
    case userConstants.LOGIN_FAILURE:
      return {};
    case userConstants.LOGOUT:
      localStorage.removeItem('user');
      return {loggedIn:false, user:{}};
    default:
      return state
  }
}