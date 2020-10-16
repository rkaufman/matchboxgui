import React from 'react';
import { connect } from 'react-redux';

export class Account extends React.Component{
    constructor(props){
        super(props);
        this.state = {

        }
    }
    render(){
        return(<h1>Account page</h1>)
    }
}
const mapStateToProps = (state, ownProps)=>{
    return{
        
    }
}
export default connect(mapStateToProps)(Account);