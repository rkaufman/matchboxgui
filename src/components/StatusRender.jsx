import { Button } from '@progress/kendo-react-buttons';
import React from 'react';

const StatusRender = props =>{
    let item = props.dataItem;
    let st = item.status === "False" ? {backgroundColor: "#323232", color:'white', backgroundImage: 'none'} : {backgroundColor: 'white', color: 'black', backgroundImage: 'none'}
    return(
        <div className="status-item-container" >
        <Button className="status-item-content-wrapper" style={st}>
            <div className="status-indicator">
                <div className="circle" style={{backgroundColor:item.status === "False"?'red':'green'}}/>
            </div>
            <span className={item.icon}/>
            <p>{item.display}</p>
            <p>{item.status === "False" ? "Disconnected": "Connected"}</p>
        </Button>
        </div>
    )
}

export default StatusRender;
