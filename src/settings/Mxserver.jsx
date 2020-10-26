import React from 'react';
import { connect } from 'react-redux';
import {ListView} from '@progress/kendo-react-listview';
import { Card, CardBody, CardTitle } from '@progress/kendo-react-layout';

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
        
    render() {
        return(<span>
                <div className="row" style={{width: '25%'}}>
                    <div style={{display: 'flex', justifyContent: 'space-evenly'}}>
                        <Card style={{width:200, backgroundColor:'#3d3d3d', color: 'white'}} orientation='horizontal'>
                            <CardBody>
                                <CardTitle><i className="fa fa-user fa-3x"/></CardTitle>
                                <CardTitle><b>Faces</b></CardTitle>
                            </CardBody>
                        </Card>
                        <Card style={{width:200, backgroundColor:'#3d3d3d', color: 'white'}} orientation='horizontal'>
                            <CardBody>
                                <CardTitle><i className="fa fa-cubes fa-3x"/></CardTitle>
                                <CardTitle><b>Objects</b></CardTitle>
                            </CardBody>
                        </Card>
                    </div>
                </div>
                <div className="row" style={{width: '25%'}}>
                   <ListView/>
                </div>
            </span>
            );
    }
}
const mapStateToProps = (state,ownProps)=>{
    return {
        history: ownProps.history
    };
}
export default connect(mapStateToProps)(Mxserver);