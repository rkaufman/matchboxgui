import { userConstants } from '../constants/userConstants';

let user = JSON.parse(localStorage.getItem('user'));
const initialState = user ? { loggedIn: true, user } : {};

export default function authentication(state = initialState, action) {
  switch (action.type) {
    case userConstants.LOGIN_REQUEST:
      return {
        loggingIn: true,
        user: action.user
      };
    case userConstants.LOGIN_SUCCESS:
      localStorage.setItem('user', {loggedIn:true, user:action.user})
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