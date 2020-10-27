import React from 'react';
import { Card, CardBody, CardTitle } from '@progress/kendo-react-layout';


class DetectionSettings extends React.Component{
    render(){
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
                   </div>
               </span>);
    }
}

export default DetectionSettings;