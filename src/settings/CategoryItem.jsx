import React from 'react';
import {DrawerItem} from '@progress/kendo-react-layout';

const CategoryItem = (props)=> {
    return(
        <DrawerItem {...props} className="setting-drawer-item">
            <span className="vertical-center" style={{ width: "100%" }}>
                <span className={props.icon} style={{ float: "left" }}/>
                <p>{props.name}</p>
            </span>
        </DrawerItem>
    );
}

export default CategoryItem;