import React from 'react';
import {ListView, ListViewHeader, ListViewFooter} from '@progress/kendo-react-listview';
import StatusRender from '../components/StatusRender';
import LogRender from '../components/LogRender';

import statuses from '../statusItems.json'
import './HomePage.css';
import { Camera } from '../components/Camera';
import {CameraPlaceHolder} from '../components/CameraPlaceHolder';

class HomePage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            logs: [{
                "status": "info",
                "text": "this is just info",
                "date": "2020-07-08 10:12:28"
            },
            {
                "status": "danger",
                "text": "this is a danger tag meaning something has gone wrong",
                "date": "2020-10-15 16:13:00"
            },
            {
                "status": "warning",
                "text": "this is a warning tag meaning something happened that may not be good",
                "date": "2020-10-15 16:14:00"
            }
        ],
            cameraStatus: "Disconnected"
        };
    }
    render() {
        return (
            <div className="row full-height">
                <div className="col-md-2 status-panel full-height">
                    <ListView data={statuses}
                        item={StatusRender}
                        className="lv-status vertical-center"/>
                </div>
                <div className="col-md-4 status-panel full-height">
                    <ListView data={this.state.logs}
                        item={LogRender}
                        className="lv-status"
                        style={{textAlign:'left'}}/>
                </div>
                <div className="col-md-6  status-panel full-height">
                    <CameraPlaceHolder className="camera-placeholder" status={this.state.cameraStatus}/>
                </div>
            </div>
        );
    }
}

export { HomePage };