// src/components/MapScreen.js
import React from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';
import MapboxGL from '@react-native-mapbox-gl/maps';

const MapScreen = () => {
  return (
    <View style={styles.container}>
      <MapboxGL.MapView style={styles.map}>
        <MapboxGL.Camera
          zoomLevel={8}
          centerCoordinate={[-122.4324, 37.78825]}
        />
        <MapboxGL.PointAnnotation
          id="marker"
          coordinate={[-122.4324, 37.78825]}
        />
      </MapboxGL.MapView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
});

export default MapScreen;