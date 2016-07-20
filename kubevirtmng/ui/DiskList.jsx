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
            url: 'http://localhost:8083/v1/volumes',
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
            <table className="datatable table table-striped table-bordered">
                <thead>
                <tr>
                  <th>Volumes</th>
                </tr>
              </thead>
               <tbody>
                  {this.state.volumes.map((volume, i) => <Volume key = {i} data = {volume} />)}
               </tbody>
            </table>
        </div>
        );
    }
}

class Volume extends React.Component {
  constructor() {
      super();

      this.state = {
         disks: []
      }

      this.fetchData = this.fetchData.bind(this);
      this.handleClick = this.handleClick.bind(this);
    };

   componentWillMount() {
      this.fetchData();
   };

  handleClick() {
    //todo : make some code to delete the disk
    console.log("click disk")
    var name = document.getElementById('disk_name').value
    var diskSize = document.getElementById('disk_size').value

    var requestData = { "size": diskSize }

    $.ajax({
            type: "POST",
            dataType: 'json',
            data: JSON.stringify(requestData),
            url: 'http://localhost:8083/v1/volumes/'+this.props.data.name+'/'+name,
            success: function(response){
              console.log(response);
              this.forceUpdate()
            }.bind(this)
           }
          );
  }

  fetchData() {
        $.ajax({
            type: "GET",
            dataType: 'json',
            url: 'http://localhost:8083/v1/volumes/'+this.props.data.name+"/",
            success: function(response){
            console.log(response);
            this.setState({disks: response.disks})
            }.bind(this)
        });

  };
  render() {
      return (
        <tr>
        <td>
          <table className="datatable table table-striped table-bordered">
            <tbody>
            <tr>
              <td>Volume:{this.props.data.name}
                <table className="datatable table table-striped table-bordered">
                   <tbody>
                      {this.state.disks.map((disk, i) => <Disk key = {i} data = {disk} volume={this.props.data.name} />)}
                   </tbody>
                </table>
              </td>
            </tr>
            <tr>
              <td>
                <form className="form-horizontal">
                  <div className="form-group">
                    <label className="col-sm-2 control-label">Disk Name</label>
                    <div className="col-sm-10">
                      <input type="text" id="disk_name" className="form-control"/>
                    </div>
                    <label className="col-sm-2 control-label">Size in Gb</label>
                    <div className="col-sm-10">
                      <input type="text" id="disk_size" className="form-control"/>
                    </div>
                  </div>
                  <div className="form-group">
                    <div className="col-sm-offset-2 col-sm-10">
                      <button type="submit" className="btn btn-primary" onClick={this.handleClick} >Add</button>
                    </div>
                  </div>
                </form>
               </td>
              </tr>
              </tbody>
          </table>
        </td>
        </tr>
      );
  }
}


class Disk extends React.Component {
   constructor() {
    super();

    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() {
    $.ajax({
            type: "DELETE",
            disableCaching: false,
            url: 'http://localhost:8083/v1/volumes/' + this.props.volume + "/" + this.props.data,
            success: function(response){
              console.log(response);
              this.forceUpdate()
              }.bind(this)
          });
    //todo : make some code to delete the disk
  }
  render() {
      return (
         <tr>
            <td>{this.props.data}</td><td>  <button type="button" className="btn btn-primary" onClick={this.handleClick} >Delete</button> </td>
         </tr>
      );
  }
}


export default DiskTable;