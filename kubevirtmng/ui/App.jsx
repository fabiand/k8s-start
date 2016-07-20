import React from 'react';
import DiskTable from'./DiskList.jsx'
import ManageVirtualMachines from './VMList.jsx'

class App extends React.Component {
   render() {
      return (
      	 <div>
			 <DiskTable />
			 <ManageVirtualMachines />
         </div>
      );
   }
}

export default App;