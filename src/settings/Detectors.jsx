import React from 'react';
import { Card, CardBody, CardTitle, CardActions } from '@progress/kendo-react-layout';
import { Button } from '@progress/kendo-react-buttons';
import { settingActions } from '../actions'
import { bindActionCreators } from "redux";
import { connect } from 'react-redux';


class Detectors extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        }
    }
    componentDidMount = () => {
        this.props.settingAction.getDetectors();
    }
    changeDetector = (e)=> {
        this.props.settingAction.changeDetector(parseInt(e.target.id));
    }
    render() {
        return (<span>
                    <div className="row" style={{ width: '75%' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-evenly' }}>
                            {this.props.detectors.map(d => {
                                let st = d.selected === true ? {width: 200, backgroundColor: 'white', color: '#3d3d3d', marginTop: '5%'} : { width: 200, backgroundColor: '#3d3d3d', color: 'white', marginTop: '5%' }
                        return(<Card style={st} orientation='horizontal'>
                                   <CardBody>
                                       <CardTitle><i className={d.icon}/></CardTitle>
                                       <CardTitle><b>{d.name}</b></CardTitle>
                                        {d.selected === true ? <span/> : <CardActions orientation='horizontal' style={{textAlign: 'center'}}><Button look='clear' onClick={this.changeDetector} id={d.id} className="card-button">Select</Button></CardActions>}
                                   </CardBody>
                               </Card>);
                    })}

                        </div>
                    </div>
                    <div className="row" style={{ width: '25%' }}>
                    </div>
                </span>);
    }
}
const mapStateToProps = (state) => {
    return {
        detectors: state.settings.detectors
    }
}
const mapDispatchToProps = (dispatch) => {
    return {
        settingAction: bindActionCreators(settingActions, dispatch)
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(Detectors);
