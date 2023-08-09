from services.flights_services import *
from api.models.flights_model import Flights


def create_mock_flight(flight_number, start_destination, end_destination, takeoff_time, landing_time, price):
    return Flights(flight_number=flight_number, start_destination=start_destination,
                   end_destination=end_destination, takeoff_time=takeoff_time,
                   landing_time=landing_time, price=price)


def test_get_all_flights(mocker):
    mock_flights = [create_mock_flight("1", "London", "Sofia", "2023-07-30 06:45", "2023-07-30 09:15", 235.70),
                    create_mock_flight("2", "Paris", "Rome", "2023-08-03 11:35", "2023-08-03 13:10", 273.40)]

    mock_query = mocker.patch('api.database.db.session.query')
    mock_query.return_value.all.return_value = mock_flights

    result = query_all_flights()
    assert len(result) == 2
    assert result[0].flight_number == '1'
    assert result[0].start_destination == 'London'
    assert result[0].end_destination == 'Sofia'
    assert result[0].takeoff_time == '2023-07-30 06:45'
    assert result[0].landing_time == "2023-07-30 09:15"
    assert result[0].price == 235.70

    assert result[1].flight_number == '2'
    assert result[1].start_destination == 'Paris'
    assert result[1].end_destination == 'Rome'
    assert result[1].takeoff_time == '2023-08-03 11:35'
    assert result[1].landing_time == "2023-08-03 13:10"
    assert result[1].price == 273.40


def test_get_user_by_uuid(mocker):
    mock_flight = create_mock_flight("1", "London", "Sofia", "2023-07-30 06:45", "2023-07-30 09:15", 235.70)
    mock_query = mocker.patch("api.database.db.session.query")

    mock_query.return_value.get.return_value = mock_flight
    result = query_flight_by_flight_number("1")
    assert result == mock_flight

    mock_query.return_value.get.return_value = None
    result = query_flight_by_flight_number("invalid_uuid")
    assert result is None


# def test_get_passengers_on_flight(mocker):
#     mock_flight_number = "FLIGHT123"
#
#     mock_passenger_data = [
#         ("1", "passenger1@example.com", "John", "Doe"),
#         ("2", "passenger2@example.com", "Jane", "Smith"),
#     ]
#
#     mock_query = mocker.patch('api.database.db.session.query')
#     mock_query.return_value.join.return_value.join.return_value.with_entities.return_value.filter_by.\
#         return_value.all.return_value = mock_passenger_data
#
#     result = get_passengers_on_flight(mock_flight_number)
#
#     assert len(result) == len(mock_passenger_data)
#
#     for i, passenger_data in enumerate(mock_passenger_data):
#         booking_id, email, first_name, last_name = passenger_data
#         assert result[i].booking_id == booking_id
#         assert result[i].email == email
#         assert result[i].first_name == first_name
#         assert result[i].last_name == last_name
#
#     mock_query.assert_called_once()
#     mock_query.return_value.join.assert_called_once_with(UserBookings.users)
#     mock_query.return_value.join.return_value.join.assert_called_once_with(UserBookings.flights)
#     mock_query.return_value.join.return_value.join.return_value.with_entities.assert_called_once_with(
#         UserBookings.booking_id, Users.id, Users.email, Users.first_name, Users.last_name
#     )
#     mock_query.return_value.join.return_value.join.return_value.with_entities.return_value.filter_by.\
#         assert_called_once_with(
#         flight_number=mock_flight_number
#     )
#     mock_query.return_value.join.return_value.join.return_value.with_entities.return_value.filter_by.return_value.all.\
#         assert_called_once()

def test_add_flight_to_db(mocker):
    mock_flight = create_mock_flight("1", "London", "Sofia", "2023-07-30 06:45", "2023-07-30 09:15", 235.70)

    mock_add = mocker.patch('api.database.db.session.add')
    mock_commit = mocker.patch('api.database.db.session.commit')

    add_flight_to_db(mock_flight)

    mock_add.assert_called_once_with(mock_flight)
    mock_commit.assert_called_once()


def test_delete_user_to_db(mocker):
    mock_flight = create_mock_flight("1", "London", "Sofia", "2023-07-30 06:45", "2023-07-30 09:15", 235.70)

    mock_add = mocker.patch('api.database.db.session.delete')
    mock_commit = mocker.patch('api.database.db.session.commit')

    delete_flight_from_db(mock_flight)

    mock_add.assert_called_once_with(mock_flight)
    mock_commit.assert_called_once()


def test_edit_user_data(mocker):
    mock_flight = create_mock_flight("1", "London", "Sofia", "2023-07-30 06:45", "2023-07-30 09:15", 235.70)

    mock_edin_json_data = {'takeoff_time': '2023-07-17 16:00', 'landing_time': '2023-07-17 18:20'}
    mock_commit = mocker.patch('api.database.db.session.commit')

    edit_flight_data(mock_flight, mock_edin_json_data)
    assert mock_flight.flight_number == "1"
    assert mock_flight.start_destination == "London"
    assert mock_flight.end_destination == "Sofia"
    assert mock_flight.takeoff_time == "2023-07-17 16:00"
    assert mock_flight.landing_time == "2023-07-17 18:20"
    assert mock_flight.price == 235.70

    mock_commit.assert_called_once()
