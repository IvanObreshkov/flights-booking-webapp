from mock import patch

def mock_decorator(func):
    return func

patch('api.utils.admin_required', mock_decorator).start()
from api.routes.crud_flights_route import get_flight
    
class TestFlightsRoute:
    class MockFlight:
        def __init__(self, obj): 
            self.__flight = obj

        def to_json(self):
            return self.__flight

    def test_flights_route__get_flight__flight_exists(self, mocker):
        flight = {"number": "some_number", "to": "somewhere", "from": "somewhere"}
        mock_flight = TestFlightsRoute.MockFlight(flight)

        mock_query = mocker.patch("api.database.db.session.query")
        mocker.patch("api.database.db.session.close")
        mock_query.return_value.get.return_value = mock_flight 

        flight_number = 5
        response, status_code = get_flight(flight_number=flight_number)

        mock_query.return_value.get.assert_called_once_with(flight_number)

        assert {"Flight": mock_flight.to_json()} == response
        assert status_code == 200
