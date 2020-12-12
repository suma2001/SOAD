// import React, { Component } from 'react';
// import GoogleMapReact from 'google-map-react';
 
// const AnyReactComponent = ({ text }) => <div><h1>{text}</h1></div>;
 
// class SimpleMap extends Component {
//   static defaultProps = {
//     center: {
//       lat: 59.95,
//       lng: 30.33
//     },
//     zoom: 11
//   };
 
//   render() {
//     console.log("Map");
//     return (
//       // Important! Always set the container height explicitly
//       <div style={{ height: '100vh', width: '100%' }}>
//         <GoogleMapReact
//           bootstrapURLKeys={{ key: "AIzaSyAEFeUBQwZ4Yz3-Dqc2vntF9G18ZNnFa9c" }}
//           defaultCenter={this.props.center}
//           defaultZoom={this.props.zoom}
//         >
//           <AnyReactComponent
//             lat={59.955413}
//             lng={30.337844}
//             text="<i class='fa fa-user'></i>"
//           />
//         </GoogleMapReact>
//       </div>
//     );
//   }
// }
 
// export default SimpleMap;


import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';
import React, { Component } from 'react';

const mapStyles = {
  width: '100%',
  height: '70%',
};

class SimpleMap extends Component {

  constructor(props) {
    super(props);

    this.state = {
      elders: []
    }
  }

  componentDidMount() {
    fetch("http://127.0.0.1:8000/api/elders/")
    .then((response) => {
      return response.json();
    })
    .then(data => {
      let elders = data.map(elder => {
        console.log(elder.location.slice(17, 33));
        return {latitude: parseFloat(elder.location.slice(17, 33)), longitude: parseFloat(elder.location.slice(34, 51))}
      });
      this.setState({
        elders: elders
      });
    })
  }

  displayMarkers = () => {
    console.log(this.state.elders);
    return this.state.elders.map((elder, index) => {
      console.log(typeof(elder.latitude));
      return <Marker key={index} id={index} position={{
       lat: elder.longitude,
       lng: elder.latitude
     }}
     onClick={() => console.log(elder)} />
    })
  }

  render() {
    return (
      <div>
        <Map
          google={this.props.google}
          zoom={5}
          style={mapStyles}
          initialCenter={{ lat: 20.5937, lng: 78.9629}}
        >
          {/* <Marker position={{ lat: 48.00, lng: -122.00}} /> */}
          {this.displayMarkers()}
        </Map>
      </div>
      
    );
  }
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyAEFeUBQwZ4Yz3-Dqc2vntF9G18ZNnFa9c'
})(SimpleMap);