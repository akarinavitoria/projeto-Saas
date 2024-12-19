// src/components/MapScreen.js
import React from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const mapContainerStyle = {
  width: '100%',
  height: '500px'
};

const center = {
  lat: -23.55052,
  lng: -46.633308
};

function MapScreen() {
  return (
    <LoadScript googleMapsApiKey="SUA_API_KEY">
      <GoogleMap mapContainerStyle={mapContainerStyle} center={center} zoom={15}>
        <Marker position={center} />
      </GoogleMap>
    </LoadScript>
  );
}

export default MapScreen;

