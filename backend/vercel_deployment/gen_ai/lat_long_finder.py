# Install geopy if you haven't already
# You can run this in your terminal or Jupyter: pip install geopy

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_coordinates(address):
    try:
        geolocator = Nominatim(user_agent="geoapi")
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            print("Address not found.")
            return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    coordinates = get_coordinates(address)
    if coordinates:
        print(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
    else:
        print("Could not retrieve coordinates.")
