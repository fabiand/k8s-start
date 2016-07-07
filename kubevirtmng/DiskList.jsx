import React from 'react';
import $ from "jquery"


class DiskTable extends React.Component {
	constructor() {
      super();

      this.state = {
         volumes: []
      }

      this.fetchData = this.fetchData.bind(this);
    };

    fetchData() {
        $.ajax({
            type: "GET",
            dataType: 'json',
            url: 'http://localhost:8084/v1/volumes',
            success: function(response){
            console.log(response);
            this.setState({volumes: response.volumes})
            }.bind(this)
        });

   };

   componentWillMount() {
   		this.fetchData();
   };


    render() {
      return (
      	<div>
            <table>
               <tbody>
                  {this.state.volumes.map((volume, i) => <Volume key = {i} data = {volume} />)}
               </tbody>
            </table>
        </div>
      	);
    }
}

class Volume extends React.Component {
   render() {
      return (
         <tr>
            <td>{this.props.data.name}</td>
         </tr>
      );
   }
}

export default DiskTable;