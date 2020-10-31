import config from './config';
import { authHeader } from '../helpers';

const startCamera = () => {
  let opt = {
    method: 'POST',
    headers: authHeader()
  };
  return fetch(`${config.apiUrl}/camera/start`, opt)
      .then((r) => {
          if (r.ok) return true;
          return Promise.reject(r.statusText);
      });
}

const stopCamera = () => {
  let opt = {
    method: 'POST',
    headers: authHeader()
  };
  return fetch(`${config.apiUrl}/camera/stop`, opt)
      .then((r) => {
          if (r.ok) return true;
          return Promise.reject(r.statusText);
      });
}
const viewCamera = (view) => {
  let opt = {
    method: 'POST',
    headers: authHeader()
  };
  return fetch(`${config.apiUrl}/camera/view?show=${view}`, opt)
    .then((r) => {
        if (r.ok) return true;
        return Promise.reject(r.statusText);
    });
}

export const cameraService = {
  startCamera,
  stopCamera,
  viewCamera
}

export default cameraService;