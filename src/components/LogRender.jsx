import React from 'react';
import LogStatusIndicator from './LogStatusIndicator';

const StatusRender = (props)=>{
    let item = props.dataItem;
    return(
        <div className="row log-container">
            <div className="col-md-1 full-height">
                <LogStatusIndicator status={item.status}/>
            </div>
            <div className="col-md-10 vertical-center">
                <p>{item.date}</p>
                <p>{item.text}</p>
            </div>
        </div>
    )
}

export default StatusRender

