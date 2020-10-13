import React from 'react';
import { connect } from 'react-redux';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import { PrivateRoute } from '../components';
import { HomePage } from '../homePage';
import { LoginPage } from '../loginPage';

class App extends React.Component {
    render() {
        return (
            <div className="jumbotron">
                <div className="container">
                    <div className="col-sm-8 col-sm-offset-2">
                        <Router>
                            <div>
                                <Route exact path="/login" component={LoginPage} />
                                <PrivateRoute exact path="/" component={HomePage} loggedIn={this.props.loggedIn}/>
                            </div>
                        </Router>
                    </div>
                </div>
            </div>
        );
    }
}
const mapStateToProps = (state)=>{
    const {loggedIn} = state.authentication;
    return{
        loggedIn
    }
}
export default connect(mapStateToProps)(App);