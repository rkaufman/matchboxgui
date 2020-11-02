import React from 'react'
import { connect } from 'react-redux'

export class Camera extends React.Component{
    render() {
        return(
            <div>
                <img src={this.props.vidSrc} id="vid" className="video-view-portal" />
            </div>
        );
    }
}
const mapStateToProps = (state, ownProps)=>{
    return{
        vidSrc: ownProps.vidSrc
    }
}
export default connect(mapStateToProps)(Camera)
