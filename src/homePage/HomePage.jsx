import React from 'react';
import {ListView} from '@progress/kendo-react-listview';
import StatusRender from '../components/StatusRender';
import LogRender from '../components/LogRender';
import {bindActionCreators} from 'redux';
import './HomePage.css';
import {CameraPlaceHolder} from '../components/CameraPlaceHolder';
import { connect } from 'react-redux';

export class HomePage extends React.Component {
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
    componentDidMount() {

    }

    render() {
        return (
            <span>
                <div className="col-md-2 status-panel full-height">
                    <ListView data={this.props.statuses}
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
            </span>
        );
    }
}

const mapStateToProps = (state,ownProps)=>{
    return {
        statuses: state.statuses,
        history: ownProps.history
    }
}

export default connect(mapStateToProps)(HomePage)
