import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import {BrowserRouter} from 'react-router-dom';
import { store } from './helpers';
import ReduxToastr from 'react-redux-toastr';
import App from './app/App';
import 'react-redux-toastr/lib/css/react-redux-toastr.min.css';
// setup fake backend
//import { configureFakeBackend } from './helpers/fake-backend';
//configureFakeBackend();

render(
    <Provider store={store}>
        <div className="full-height">
            <BrowserRouter>
                <App />
            </BrowserRouter>
            <ReduxToastr
                timeOut={4000}
                newestOnTop={false}
                preventDuplicates
                position="top-left"
                getState={(state)=> state.toastr}
                transitionIn="fadeIn"
                transitionOut="fadeOut"
                progressBar
                closeOnToastrClick/>
        </div>
    </Provider>,
    document.getElementById('root')
);