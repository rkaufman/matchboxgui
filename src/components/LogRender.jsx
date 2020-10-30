import React from 'react';
import LogStatusIndicator from './LogStatusIndicator';
import Datetime from 'react-datetime';


const StatusRender = (props)=>{
    let item = props.dataItem;
    return(
        <div className="row log-container">
            <div className="col-md-1 full-height">
                <LogStatusIndicator status={item.msgType}/>
            </div>
            <div className="col-md-10 vertical-center">
                <p>{new Date(item.date).toLocaleDateString() + ' ' + new Date(item.date).toLocaleTimeString()}</p>
                <p>{item.message}</p>
            </div>
        </div>
    )
}

export default StatusRender

