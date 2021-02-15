from pydantic.main import BaseModel


class Hotel(BaseModel):
    name: str
    city: str
    state: str
    avg_rating: str
    review: str
    price: str


class Flight(BaseModel):
    date: str
    carrier: str
    airport_name: str
    airport_city: str
    airport_state: str
    price: str
    departure_hour: str
    arrival_hour: str


class FlightFrom(BaseModel):
    uname: str
    origin_airport_id: str
    passengers: str


class Person(BaseModel):
    uname: str
    password: str


class Attraction(BaseModel):
    name: str
    location: str
    picture_link: str


class Name(BaseModel):
    uname: str


class AllAttraction(BaseModel):
    att1: Attraction
    att2: Attraction
    att3: Attraction


class Travel(BaseModel):
    going_flight: Flight
    return_flight: Flight
    hotel: Hotel
    attractions: AllAttraction
    passengers: str
    origin_airport_id: str


class Save(BaseModel):
    uname: str
    trip: Travel

