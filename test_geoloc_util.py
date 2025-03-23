import pytest
from fetching.geoloc_util import get_city_data, get_city_data_by_zip, fetch_city_data_for_locations, CityData

# Sample test data for parameterization
city_state_data = [
    # Valid city/state combinations
    ("Los Angeles", "CA", CityData('Los Angeles', 34.0536909, -118.242766, 'US')),
    ("New York", "NY", CityData('New York', 40.7127281, -74.0060152, 'US')),
    ("Chicago", "IL", CityData('Chicago', 41.8755616, -87.6244212, 'US')),
    
    # Invalid city/state
    ("InvalidCity", "CA", None),
]

zip_code_data = [
    # Valid zip codes
    ("98115", "US", CityData('Seattle', 47.6849, -122.2968, 'US')),
    ("30301", "US", CityData('Cobb County', 33.8444, -84.4741, 'US')),
    
    # Invalid zip code
    ("99999", "US", None),
    
    # Edge case: empty input
    ("", "", None),
]

# Test for city/state data
@pytest.mark.parametrize("city, state, expected", city_state_data)
def test_get_city_data(city, state, expected):
    result = get_city_data(city, state)
    
    if expected is None:
        assert result is None  # Expecting None for invalid cases
    else:
        assert isinstance(result, CityData)  # Check if result is an instance of CityData
        assert result.name == expected.name
        assert result.lat == expected.lat
        assert result.lon == expected.lon
        assert result.country == expected.country

# Test for zip code data
@pytest.mark.parametrize("zip_code, country, expected", zip_code_data)
def test_get_city_data_by_zip(zip_code, country, expected):
    result = get_city_data_by_zip(zip_code, country)
    
    if expected is None:
        assert result is None  # Expecting None for invalid cases
    else:
        assert isinstance(result, CityData)  # Check if result is an instance of CityData
        assert result.name == expected.name
        assert result.lat == expected.lat
        assert result.lon == expected.lon
        assert result.country == expected.country

# Sample test data for multiple locations
multiple_locations_data = [
    (["Los Angeles, CA", "New York, NY"], [
        CityData('Los Angeles', 34.0536909, -118.242766, 'US'),
        CityData('New York', 40.7127281, -74.0060152, 'US')
    ]),
    (["98115", "30301"], [
        CityData('Seattle', 47.6849, -122.2968, 'US'),
        CityData('Cobb County', 33.8444, -84.4741, 'US')
    ]),
]

@pytest.mark.parametrize("locations, expected", multiple_locations_data)
def test_fetch_city_data_for_locations(locations, expected):
    results = fetch_city_data_for_locations(locations)
    
    for result, exp in zip(results, expected):
        assert isinstance(result, CityData)  # Check if result is an instance of CityData
        assert result.name == exp.name
        assert result.lat == exp.lat
        assert result.lon == exp.lon
        assert result.country == exp.country

# Separate test for invalid city cases
@pytest.mark.parametrize("locations", [["InvalidCity, CA"], ["99999"]])
def test_fetch_city_data_for_invalid_locations(locations):
    results = fetch_city_data_for_locations(locations)
    
    for result in results:
        assert result is None  # Expecting None for invalid cases 