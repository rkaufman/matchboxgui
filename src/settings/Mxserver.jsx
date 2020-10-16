import React from 'react';
import { connect } from 'react-redux';
import {ListView} from '@progress/kendo-react-listview';

export class Mxserver extends React.Component{
    constructor(props){
        super(props);
        this.state = {
        }
    }
    //TODO: get from db
    items = [
        {}
    ]
    onSelect = (e)=>{
    }
        
    render(){
        return(<ListView/>)
    }
}
const mapStateToProps = (state,ownProps)=>{
    return {
        history: ownProps.history
    };
}
export default connect(mapStateToProps)(Mxserver);