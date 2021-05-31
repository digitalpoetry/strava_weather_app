import re
import time

import pytest

import manage_db
import utilities

LAT = 55.752388  # Moscow latitude default
LON = 37.716457  # Moscow longitude default
TIME = int(time.time() - 3600)

directions_to_try = [(0, 'N', 'С'), (7, 'N', 'С'), (11, 'N', 'С'), (12, 'NNE', 'ССВ'),
                     (33, 'NNE', 'ССВ'), (85, 'E', 'В'), (358, 'N', 'С'), (722, 'N', 'С')]
directions_ids = [f'{d[0]:<3}: {d[1]:>3}' for d in directions_to_try]


@pytest.mark.parametrize('degree, direction_en, direction_ru', directions_to_try, ids=directions_ids)
def test_compass_direction(degree, direction_en, direction_ru):
    """Should return correct direction in english and russian"""
    assert utilities.compass_direction(degree) == direction_en
    assert utilities.compass_direction(degree, 'ru') == direction_ru


def test_is_app_subscribed():
    """Should return boolean"""
    check_supscription = utilities.is_app_subscribed()
    assert isinstance(check_supscription, bool)


def test_get_weather_pictogram():
    icon = utilities.get_weather_icon(LAT, LON, TIME)
    print(icon)
    assert isinstance(icon, str)
    assert len(icon) == 1


def test_get_weather_description():
    settings = manage_db.DEFAULT_SETTINGS
    descr = utilities.get_weather_description(LAT, LON, TIME, settings)
    print(descr)
    assert re.fullmatch(r'(\w+\s?){1,3}, 🌡.-?\d{1,2}°C \(по ощущениям -?\d{1,2}°C\), '
                        r'💦.\d{1,3}%, 💨.\d{1,2}м/с \(с \w{1,3}\).', descr)


def test_get_air_description():
    description = utilities.get_air_description(LAT, LON, lan='ru')
    print(description)
    assert re.fullmatch(r'\nВоздух . \d+\(PM2\.5\), \d+\(SO₂\), \d+\(NO₂\), \d+(\.\d)?\(NH₃\)\.', description)


@pytest.mark.parametrize('activity_type', [{'manual': True}, {'trainer': True}, {'type': 'VirtualRide'}])
def test_manual_act(activity_type, monkeypatch):
    """Return 3 if activity is manual, trainer or VirtualRider"""
    class StravaClientMock:
        def __init__(self, athlete_id, activity_id):
            self.athlete_id = athlete_id
            self.activity_id = activity_id

        @staticmethod
        def get_activity():
            return activity_type

    monkeypatch.setattr(utilities, 'StravaClient', StravaClientMock)
    assert utilities.add_weather(0, 0) == 3


@pytest.mark.skip(reason='Not implemented yet')
class TestAddWeather:
    """Test add_weather function"""

    def test_manual_indoor_activities(self):
        pass
        # assert utilities.add_weather(0, 0) == 3

    def test_activity_with_weather(self):
        """Return 3 if weather information already added in activity"""
        pass

    def test_activity_without_coordinates(self):
        """Return 3 if activity doesn't contains latitude and longitude"""
        pass
