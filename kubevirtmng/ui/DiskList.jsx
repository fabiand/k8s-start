import React from 'react';
import $ from "jquery"


class Volume extends React.Component {
  constructor() {
      super();

      this.state = {
         disks: []
      }

      this.fetchData = this.fetchData.bind(this);
    };

   componentWillMount() {
      this.fetchData();
   };

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
                      {this.state.disks.map((disk, i) => <Disk key = {i} data = {disk} />)}
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
                      <input type="text" id="name" className="form-control"/>
                    </div>
                    <label className="col-sm-2 control-label">Size in Gb</label>
                    <div className="col-sm-10">
                      <input type="text" id="size" className="form-control"/>
                    </div>
                  </div>
                  <div className="form-group">
                    <div className="col-sm-offset-2 col-sm-10">
                      <button type="submit" className="btn btn-primary">Add</button>
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


class Disk extends React.Component {
   constructor() {
    super();

    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() {
    //todo : make some code to delete the disk
  }
  render() {
      return (
         <tr>
            <td>Disk:{this.props.data}</td><td>  <button type="button" className="btn btn-primary">Delete</button> </td>
         </tr>
      );
  }
}


export default DiskTable;