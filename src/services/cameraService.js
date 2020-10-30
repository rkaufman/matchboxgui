import {serviceBase} from "./serviceBase";
import config from './config';
import { authHeader } from '../helpers';

const startCamera = () => {
  let opt = {
    method: 'POST',
    headers: authHeader()
  };
  return fetch(`${config.apiUrl}/camera/start`, opt)
    .then(serviceBase.handleResponse)
    .then(() => {
      return true;
    });
}

const stopCamera = () => {
  let opt = {
    method: 'POST',
    headers: authHeader()
  };
  return fetch(`${config.apiUrl}/camera/stop`, opt)
    .then(serviceBase.handleResponse)
    .then(() => {
      return true;
    });
}
const viewCamera = (view) => {
  let opt = {
    method: 'POST',
    headers: authHeader()
  };
  return fetch(`${config.apiUrl}/camera/view?show=${view}`, opt)
    .then(serviceBase.handleResponse)
    .then(() => {
      return true;
    });
}

export const cameraService = {
  startCamera,
  stopCamera,
  viewCamera
}

export default cameraService;