import React from 'react';

const LogStatusIndicator = (props)=>{
    switch(props.status){
        case 'info':
            return (<div className="log-status-indicator" style={{backgroundColor:'#00ffb1'}}></div>);
        case 'warning':
            return (<div className="log-status-indicator" style={{backgroundColor:'#dfff00'}}/>);
        case 'error':
            return(<div className="log-status-indicator" style={{ backgroundColor: '#ff0045' }}/>);
        default:
            return(<div className="log-status-indicator" style={{backgroundColor:'#00e7ff'}}/>);
        
    }
}

export default LogStatusIndicator;