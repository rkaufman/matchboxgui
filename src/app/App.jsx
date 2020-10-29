import React from 'react';
import { withRouter } from 'react-router';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
import Header from '../components/Header';
import  PrivateRoute from '../components/PrivateRoute';
import  HomePage from '../homePage/HomePage';
import LoginPage from '../loginPage/LoginPage';
import './App.css'
import '@progress/kendo-theme-default'
import Account from '../account/Account';
import Settings from '../settings/Settings';

class App extends React.Component {
    constructor(props){
        super(props);
        this.state = {

        }
        
    }
    componentDidMount() {
        if (this.props.loggedIn === true) {

        }
    }
    render() {
        if(this.props.loggedIn){
            return (
                <div className="container mb-container full-height App">
                    <div className="row">
                        <Header/>
                    </div>
                    <div className="row full-height">
                        <Switch>
                            <PrivateRoute exact path="/" component={HomePage} loggedIn={this.props.loggedIn}/>
                            <PrivateRoute path="/status" component={HomePage} loggedIn={this.props.loggedIn}/>
                            <PrivateRoute path="/account" component={Account} loggedIn={this.props.loggedIn}/>
                            <PrivateRoute path="/settings" component={Settings} loggedIn={this.props.loggedIn} />
                        </Switch>
                    </div>
                </div>
            );
        } else{
            return (
                <div className="container mb-container full-height App">
                    <div className="row full-height">
                        <Switch>
                            <PrivateRoute exact path="/" component={HomePage} loggedIn={this.props.loggedIn}/>
                            <PrivateRoute path="/status" component={HomePage} loggedIn={this.props.loggedIn}/>
                            <PrivateRoute path="/account" component={Account} loggedIn={this.props.loggedIn}/>
                            <PrivateRoute path="/settings" component={Settings} loggedIn={this.props.loggedIn} />
                            <Route exact path="/login" component={LoginPage} />
                        </Switch>
                    </div>
                </div>
            );
        }
    }
}
const mapStateToProps = (state, ownProps)=>{
    const {loggedIn} = state.authentication;
    
    return{
        loggedIn,
        history: ownProps.history
    }
}
export default withRouter(connect(mapStateToProps)(App));