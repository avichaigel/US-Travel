import uvicorn
from starlette.responses import JSONResponse
from items import *
from connect import *
import json

# parm: person
# ret: all the person table
# The user click on sign_up
@app.post('/api/sign_up')
def sigh_up(person: Person):
    check = "select * from us_travel.person where name = '" + str(person.uname) + "'"
    mycursor.execute(check)
    check = mycursor.fetchall()
    if check:
        return Response("this user name already exist", status_code=400)
    else:
        insert = "INSERT INTO `us_travel`.`person` (`name`, `password`) VALUES ('" + person.uname + "', '" + person.password + "');"
        mycursor.execute(insert)
        MY_DB.commit()
        return JSONResponse(status_code=200)


# parm: person
# ret: all the person table
# The user click on sign_in
@app.post('/api/sign_in')
def sigh_in(person: Person):
    # if there is no name like that
    check = "select * from us_travel.person where name = '" + person.uname + "' and password = '" + person.password + "'"
    mycursor.execute(check)
    check = mycursor.fetchall()
    if not check:
        return JSONResponse("something is wrong, the username or password are incorrect", status_code=400)
    else:
        return JSONResponse(status_code=200)


# parm: person
# The user what us delete from the DB
@app.delete('/api/delete_person')
def delete(person: Person):
    sql = "DELETE FROM us_travel.save_travels WHERE (`password` = '" + str(
        person.password) + "') and (`name` = '" + person.uname + "');"
    mycursor.execute(sql)
    MY_DB.commit()


# parm: flight_from
# ret: flight for the user according his ask
# The user click on flight
@app.post('/api/lucky')
def find_travel(flight_from: FlightFrom):
    flight_1 = []
    flight_2 = []
    hotel = []
    attraction = []
    # get travel when you have all the travel
    while not hotel or not flight_1 or not flight_2 or not attraction or len(attraction) != 3:
        city = "SELECT city,state FROM us_travel.airports where airport_id = '" + flight_from.origin_airport_id + "';"
        mycursor.execute(city)
        result2 = mycursor.fetchall()

        city = result2[0][0]
        state = result2[0][1]

        # flight_1 = "SELECT"\
        #             " *  FROM team01.save_travels  "\
        #             " INNER JOIN  team01.flight "\
        #             " ON team01.save_travels.return_flight_id"\
        #             " =team01.flight.flight_if"\
        #             " where team01.save_travels.person_id =  "\
        #             " (select idperson from team01.person where name = '"+str(flight_from.uname)+"') "\
        #             " and team01.flight.arrive =  "\
        #             "(select id_city from team01.city where id_state = "\
        #             "(select id_state from team01.city where name = '"+str(+"'"\
        #             "limit 1)limit 1"\
        #             ")limit 1"
        # mycursor.execute(flight_1)
        # flight_1 = mycursor.fetchall()
        #
        # if not flight_1:
        flight_1 = "SELECT * FROM us_travel.flight where" \
                    " arrive = (select id_city from us_travel.city where name = " \
                    "'" + city + "') " \
                                 " order by rand()" \
                                 " limit 1; " \
                                 ""

        mycursor.execute(flight_1)
        flight_1 = mycursor.fetchall()

        dest_city = "SELECT name FROM us_travel.city where id_city = '" + str(flight_1[0][2]) + "';"
        mycursor.execute(dest_city)
        dest_city = mycursor.fetchall()
        dest_city = dest_city[0][0]

        dest_state = "select short from us_travel.state where id_state = " \
                     "(select id_state from us_travel.city where id_city = '" + str(flight_1[0][2]) + "') ;"
        mycursor.execute(dest_state)
        dest_state = mycursor.fetchall()
        dest_state = dest_state[0][0]

        flight_3 = "SELECT * FROM us_travel.flight where" \
                        " arrive = '" + str(flight_1[0][3]) + "' and dest = '" + str(flight_1[0][2]) + "'" \
                                                                                                       " order by rand()" \
                                                                                                       " limit 1"

        mycursor.execute(flight_3)
        flight_2 = mycursor.fetchall()

        # if there is hotel from his favorite  user hotel
        hotel = "SELECT us_travel.hotel.id_hotel " \
                         " FROM us_travel.save_travels"\
                         "  INNER JOIN  us_travel.hotel"\
                         " ON us_travel.save_travels.id_hotel=us_travel.hotel.id_hotel"\
                         " where us_travel.save_travels.person_id = "\
                         " (select idperson from us_travel.person where name = '"+str(flight_from.uname)+"')"\
                         " and us_travel.hotel.id_city = "\
                         " (select id_city from us_travel.city where name = '"+str(dest_city)+"')"
        mycursor.execute(hotel)
        hotel = mycursor.fetchall()

        # if not, find the lowest price (do that random to get new trip all click)
        if not hotel:
            hotel = "SELECT "\
                    "us_travel.hotel.id_hotel "\
                    "FROM us_travel.hotel "\
                    "INNER JOIN  us_travel.city "\
                    "ON us_travel.city.id_city=us_travel.hotel.id_city "\
                    "where us_travel.city.id_city =" \
                    "(select id_city from us_travel.city where name = '"+str(dest_city)+"') "\
                    "order by rand() "\
                    "limit 1"

            mycursor.execute(hotel)
            hotel = mycursor.fetchall()

        # also random
        attraction = "SELECT id_attraction,type,image FROM us_travel.attraction_1 " \
                     "where " \
                    "state =  (select id_state from us_travel.state where short = '" + str(
            dest_state) + "') " \
                          "order by rand() " \
                          "limit 3"

        mycursor.execute(attraction)
        attraction = mycursor.fetchall()

    # update
    id_hotel = str(hotel[0][0])
    going_flight_id = str(flight_1[0][0])
    return_flight_id = str(flight_2[0][0])
    attraction1_id = str(attraction[0][0])
    attraction2_id = str(attraction[1][0])
    attraction3_id = str(attraction[2][0])

    person_id = "SELECT person_id FROM us_travel.last_tripe where person_id = " \
                "((select idperson from us_travel.person where name = '" + str(flight_from.uname) + "')) ;"

    mycursor.execute(person_id)
    person_id = mycursor.fetchall()

    if not person_id:
        insert = "INSERT INTO `us_travel`.`last_tripe` (`person_id`) VALUES " \
                 "((select idperson from us_travel.person where name = '" + str(flight_from.uname) + "'));"
        mycursor.execute(insert)
        MY_DB.commit()

    update = "UPDATE `us_travel`.`last_tripe` SET `id_hotel`" \
             " = '" + id_hotel + "', `going_flight_id` = '" + going_flight_id + "', `return_flight_id` = '" + return_flight_id + "', " \
             " `attraction1_id` = '" + attraction1_id + "', `attraction2_id` = '" + attraction2_id + "', `attraction3_id` = '" + attraction3_id + "'," \
             " `passangers` = '" + str( flight_from.passengers) + "' " \
             " WHERE (`person_id` = " \
             "(select idperson from us_travel.person where name = '" + str(flight_from.uname) + "'));"

    mycursor.execute(update)
    MY_DB.commit()
    y = Name(uname=flight_from.uname)
    x = get_last_travel(y)
    return return_JSON(x)


def id_attraction(type, image):
    att1 = "SELECT id_attraction FROM us_travel.attraction_1 where  image = '" + image + "' limit 1;"
    mycursor.execute(att1)
    att1 = mycursor.fetchall()

    return att1


# parm: travel
# ret: -
# The user want to save his travel
@app.post("/api/save")
def save(save: Save):
    hotel = "SELECT id_hotel FROM us_travel.hotel where name = '" + save.trip.hotel.name + "';"
    mycursor.execute(hotel)
    hotel = mycursor.fetchall()

    flight_1 = "SELECT flight_if FROM us_travel.flight " \
               "where date = '" + str(save.trip.going_flight.date) + "'" \
               "and price = '" + str(save.trip.going_flight.price) + "'" \
               " ;"

    mycursor.execute(flight_1)
    flight_1 = mycursor.fetchall()

    flight_2 = "SELECT flight_if FROM us_travel.flight where " \
               "date = '" + str(save.trip.return_flight.date) + "' and " \
               "price = '" + str(save.trip.return_flight.price) + "' " \
               " ;"

    mycursor.execute(flight_2)
    flight_2 = mycursor.fetchall()

    person_name = "SELECT * FROM us_travel.person where name = '" + save.uname + "';"
    mycursor.execute(person_name)
    person_name = mycursor.fetchall()

    attraction_1 = id_attraction(save.trip.attractions.att1.name, save.trip.attractions.att1.picture_link)[0][0]
    attraction_2 = id_attraction(save.trip.attractions.att2.name, save.trip.attractions.att2.picture_link)[0][0]
    attraction_3 = id_attraction(save.trip.attractions.att3.name, save.trip.attractions.att3.picture_link)[0][0]

    # save the info inside save travel table
    insert = "INSERT INTO `us_travel`.`save_travels`" \
             " (`id_hotel`, `going_flight_id`, `return_flight_id`, `attraction1_id`, `attraction2_id`, " \
             " `attraction3_id`, `person_id`, `passangers`) " \
             " VALUES ('" + str(hotel[0][0]) + "', '" + str(flight_1[0][0]) + "', '" + str(
        flight_2[0][0]) + "', '" + str(attraction_1) + "'," \
                                                       " '" + str(attraction_2) + "', '" + str(
        attraction_3) + "', '" + str(person_name[0][0]) + "', '" + str(save.trip.passengers) + "');"

    mycursor.execute(insert)
    MY_DB.commit()


@app.post("/api/last")
def get_last_travel_API(name: Name):
    check = "SELECT * FROM us_travel.last_tripe where person_id = (select idperson from us_travel.person where name = '" + name.uname + "');"
    mycursor.execute(check)
    check = mycursor.fetchall()

    if not check:
        return JSONResponse("there isn't saves trip yet", status_code=400)
    x = (get_last_travel(name))
    return return_JSON(x)


def return_JSON(x):
    var_flight_return = vars(x.return_flight)
    var_flight_going = vars(x.going_flight)
    var_hotel = vars(x.hotel)
    var_att = {
        "att1": vars(x.attractions.att1),
        "att2": vars(x.attractions.att2),
        "att3": vars(x.attractions.att3)
    }
    dictio = {"going_flight": var_flight_going,
              "return_flight": var_flight_return,
              "going_flight": var_flight_going,
              "hotel": var_hotel,
              "attractions": var_att,
              "passengers": x.passengers,
              "origin_airport_id": x.origin_airport_id
              }
    return json.dumps(dictio)


# parm: name
# ret: the lsat trip that save
def get_last_travel(name: Name):

    check = "SELECT * FROM us_travel.last_tripe where person_id = (select idperson from us_travel.person where name = '" + name.uname + "');"
    mycursor.execute(check)
    check = mycursor.fetchall()

    if not check:
        return JSONResponse("there isn't saves trip yet", status_code=400)

    passengers = "SELECT passangers FROM us_travel.last_tripe where person_id='" + str(check[0][0]) + "';"
    mycursor.execute(passengers)
    passengers = mycursor.fetchall()

    last_tripe_str = "SELECT * FROM us_travel.last_tripe where " \
                     "person_id = " \
                     "(select idperson from us_travel.person where name = '" + name.uname + "');"

    mycursor.execute(last_tripe_str)
    last_tripe_str = mycursor.fetchall()

    hotel = "SELECT * FROM us_travel.hotel where " \
            "id_hotel = '" + str(last_tripe_str[0][1]) + "';"

    mycursor.execute(hotel)
    hotel = mycursor.fetchall()

    hotel_city = "SELECT name,id_state FROM us_travel.city where id_city = '" + str(hotel[0][2]) + "'"
    mycursor.execute(hotel_city)
    hotel_city = mycursor.fetchall()

    state = "SELECT name FROM us_travel.state where id_state = '" + str(hotel_city[0][1]) + "' "
    mycursor.execute(state)
    state = mycursor.fetchall()

    review = "SELECT score,titel FROM us_travel.reviews where hotel_id = '" + str(hotel[0][0]) + "';"
    mycursor.execute(review)
    review = mycursor.fetchall()

    if not review:
        review = [["4.5", "WOW!"], []]
    # if (len(str(review[0][0]))) > 4:
    #     r = (float(review[0][0]))
    #     r = round(r, 2)
    #     r = str(r)
    # else:
    #     r = review[0][0]
    # else:
    #     flo = float(review[0][0])
    #     review[0][0] = str(float("{:.2f}".format(flo))
    hotel = Hotel(name=hotel[0][1], city=hotel_city[0][0], state=state[0][0], avg_rating=review[0][0],
                  review=review[0][1], price=hotel[0][3])
    flight_1 = get_flight(last_tripe_str[0][2])
    flight_2 = get_flight(last_tripe_str[0][3])
    all_attraction = AllAttraction(att1=attraction(last_tripe_str[0][4], state[0][0]),
                                   att2=attraction(last_tripe_str[0][5], state[0][0]),
                                   att3=attraction(last_tripe_str[0][6], state[0][0]))

    original_airport = "SELECT * FROM us_travel.airports where city = '" + str(
        flight_2.airport_city) + "' and state = '" + str(flight_2.airport_state) + "';"
    mycursor.execute(original_airport)
    original_airport = mycursor.fetchall()

    travel = Travel(hotel=hotel, going_flight=flight_1, return_flight=flight_2, attractions=all_attraction,
                    passengers=str(passengers[0][0]), origin_airport_id=str(original_airport[0][0]))
    return travel


def attraction(id, location):
    attraction = "SELECT type,image,location FROM us_travel.attraction_1" \
                 " where id_attraction = '" + str(id) + "';"
    mycursor.execute(attraction)
    attraction_1 = mycursor.fetchall()
    return Attraction(name=attraction_1[0][0], location=attraction_1[0][2], picture_link=attraction_1[0][1])


def get_flight(airport_id):
    flight_1 = "SELECT * FROM us_travel.flight where flight_if = '" + str(airport_id) + "';"
    mycursor.execute(flight_1)
    flight_1 = mycursor.fetchall()

    airport = "SELECT name,city,state FROM us_travel.airports where city = " \
              " (select name from us_travel.city where id_city = '" + str(flight_1[0][2]) + "' );"
    mycursor.execute(airport)
    airport = mycursor.fetchall()

    departure_hour = str(flight_1[0][5])
    print(departure_hour)

    if not ":" in departure_hour:
        while len(departure_hour) < 4:
            departure_hour = "0" + departure_hour

        departure_hour = departure_hour[0:2] + ":" + departure_hour[2:4]

    arrival_hour = str(flight_1[0][6])
    print(arrival_hour)
    if not ":" in arrival_hour:

        while len(arrival_hour) < 4:
            arrival_hour = "0" + arrival_hour

        arrival_hour = arrival_hour[0:2] + ":" + arrival_hour[2:4]


    return Flight(date=str(flight_1[0][1]), carrier="", airport_name=str(airport[0][0]),
                  airport_city=str(airport[0][1]),
                  airport_state=str(airport[0][2]), price=str(flight_1[0][4]),
                  departure_hour=departure_hour, arrival_hour=arrival_hour)


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8080)
