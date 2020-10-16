import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';
import { createLogger } from 'redux-logger';
import rootReducer from '../reducers';
import {routerMiddleware} from 'react-router-redux';
import reduxImmutableStateInvariant from 'redux-immutable-state-invariant';

const loggerMiddleware = createLogger();

export default function configureStore(history){
    return createStore(
        rootReducer,
        applyMiddleware(
            thunkMiddleware,
            loggerMiddleware,
            routerMiddleware(history),
            reduxImmutableStateInvariant()
        )
    );
}
