import React from 'react';
import { StyleSheet, View } from 'react-native';
import MapboxGL from '@react-native-mapbox-gl/maps';

// Defina o token de acesso
MapboxGL.setAccessToken('YOUR_MAPBOX_ACCESS_TOKEN');

const MapScreen = () => {
  return (
    <View style={styles.container}>
      <MapboxGL.MapView style={styles.map}>
        <MapboxGL.Camera
          zoomLevel={12}
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
