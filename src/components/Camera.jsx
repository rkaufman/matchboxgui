import React from 'react'
import { connect } from 'react-redux'

export class Camera extends React.Component{
    render() {
        return(
            <div></div>
        );
    }
}
const mapStateToProps = (state, ownProps)=>{
    return{
        
    }
}
export default connect(mapStateToProps)(Camera)