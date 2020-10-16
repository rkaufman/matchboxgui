import { Button } from '@progress/kendo-react-buttons';
import React from 'react';

const StatusRender = props =>{
    let item = props.dataItem;
    return(
        <div className="status-item-container">
        <Button className="status-item-content-wrapper">
            <div className="status-indicator">
                <div className="circle" style={{backgroundColor:item.state === 'red'?'red':'green'}}/>
            </div>
            <i className={item.icon} aria-hidden="true"/>
            <p>{item.text}</p>
            <p>{item.status}</p>
        </Button>
        </div>
    )
}

export default StatusRender;