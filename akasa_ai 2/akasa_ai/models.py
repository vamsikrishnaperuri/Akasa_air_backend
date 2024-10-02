from pymongo import ReturnDocument
from helpers import *
from fares import *
user_data_json = '''{
    "name": "Harsha Bellala",
    "date_of_birth": "1990-05-15T00:00:00",
    "passportNumber": "A12345678",
    "joined_akasa": "2024-05",
    "membershipNumber": "AA12345",
    "home_city": "Hyderabad",
    "home_airport_code": "HYD",
    "most_preferred_class": "Economy",
    "email": "harshasrikasyap807@gmail.com",
    "phone": "+919876543210",
    "nationality": "Indian"
}'''
from bson import ObjectId

# Custom JSON encoder for ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class FlightBookingSystem:
    def __init__(self):
        
        self.freeseats = None
        self.completedcalls = {"nfd" :False, "ns" : False ,"nfc" : False , 'rfp' : False , "need-new-flights-data" : ""}
        self.fc = None
    def reset (self):
        self.completedcalls['nfd'] = False
        self.completedcalls['ns'] = False
        self.completedcalls['nfc'] = False
        self.completedcalls['rfp'] = False
        self.completedcalls['need-new-flights-data'] = ""

    def classify_intent(self, ai_res):
        self.ai_res = ai_res
        if "booking" in self.ai_res:
            return "booking", ai_res
        
        elif "change_flight" in self.ai_res:
            return "change_flight", ai_res
        elif "cancelling" in self.ai_res:
            return "cancelling", ai_res
        elif "flight_info" in self.ai_res:
            return "flight_info", ai_res
        # elif "cancelling" in self.ai_res and self.ai_res["cancelling"]:
        #     return self.handle_cancellation(self.ai_res['cancelling'])

        elif "flight_info" in self.ai_res and self.ai_res["flight_info"]:
            return self.handle_flight_info(self.ai_res['flight_info'])

        

        elif "change_preferences" in self.ai_res and self.ai_res["change_preferences"]:
            return self.handle_change_preferences(self.ai_res['change_preferences'])

        else:
            return {'intent': 'unknown'}
    def handle_intent(self, ai_res, intent):
        self.ai_res = ai_res
        if "booking" == intent:
            return self.handle_booking(self.ai_res)

        elif "cancelling" == intent : 
            return self.handle_cancellation(self.ai_res['cancelling'])

        elif "flight_info" == intent:
            return self.handle_flight_info(self.ai_res['flight_info'])

        elif "change_flight" == intent:
            return self.handle_change_flight(self.ai_res['change_flight'])

        elif "change_preferences" == intent :
            return self.handle_change_preferences(self.ai_res['change_preferences'])

        else:
            return {'intent': 'unknown'}

    def handle_booking(self,chat_session, booking_info):
        try : 
            if booking_info.get("need-flights-data",'no').lower()  == 'no':
                self.completedcalls['nfd'] = False
            if booking_info.get("need-seat-data",'no').lower()  == 'no':
                self.completedcalls['ns'] = False
            if booking_info.get("need-flight-cost",'no').lower()  == 'no':
                self.completedcalls['nfc'] = False
            if booking_info.get("readyforpayment",'no').lower()  == 'no':
                self.completedcalls['rfp'] = False

            if booking_info.get("readyforpayment",'no').lower()  == 'yes' and not self.completedcalls['rfp'] :
                print(booking_info)
                input_json = json.dumps(booking_info)
                booking_payload = create_booking_payload(input_json, user_data_json)
                print(booking_payload)
                result = chat_session.collection_flight_bookings.insert_one(booking_payload)
                
                response = chat_session.chat.send_message("from Admin : booking is completed share booking reference to user and thanks for using assitant and booking details are  :  " + json.dumps(booking_payload,cls=JSONEncoder) )
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                self.completedcalls['rfp'] = True
                return jres 
            if booking_info.get("need-flight-cost",'no').lower()  == 'yes' and not self.completedcalls['nfc'] :
                
                            
                source = booking_info.get("source",None)
                destination = booking_info.get("destination",None)
                seat_number = booking_info.get("seat",None)
                seat_type = None
                if seat_number:
                    seat_type = classify_seat(seat_number)
                if source and destination and seat_type :
                    meal = booking_info.get("meal",None)
                    mealflag = False
                    if meal and meal !=  "not-applicable":
                        mealflag = True
                    fare, mealprice = get_flight_fare(source, destination, seat_type, mealflag)
                    


                    response = chat_session.chat.send_message("from Admin : flight fare :  " + str(fare) + ", mealfare : " + str(mealprice) )
                    response_message= ""
                    for c in response:
                        response_message += c.text
                    
                    extracted_json = extract_json_from_string(response_message)
                    jres = json.loads(extracted_json)
                    self.completedcalls['nfc'] = True
                    return jres
            if booking_info.get("need-seat-data",'no').lower()  == 'yes' and not self.completedcalls['ns'] :
                if not self.freeseats:
                    self.freeseats = generate_airplane_seats()
                seats = json.dumps(self.freeseats)

                
                response = chat_session.chat.send_message("unbooked Seats Data from admin :  " + seats)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                self.completedcalls['ns'] = True
                return jres
            
            if booking_info.get("need-flights-data",'no').lower()  == 'yes' and not self.completedcalls['nfd']:
                self.freeseats = None
                source = booking_info.get("source",None)
                destination = booking_info.get("destination",None)
                departure_date = booking_info.get("dateofdeparture",None)
                flight_data = "No flight for the source and destination on the routes on the day please ask the user for different dates"
                if source and destination and departure_date:
                    flight_data = get_flights(chat_session.collection_flight_dates,source,destination,departure_date)
                    if len(flight_data["flights"]) == 0:
                        flight_data = "No flight for the source and destination on the routes on the day please ask the user for different dates"
                    else:   
                        flight_data = json.dumps(flight_data)
                
                response = chat_session.chat.send_message("Flights Data from admin :  " + flight_data)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                self.completedcalls['nfd'] = True
                return jres
            
            
            print('rfp',booking_info.get("readyforpayment",'no').lower() )
            
        except Exception as e:
        
            self.completedcalls['nfd'] = False
            self.completedcalls['ns'] = False
            self.completedcalls['nfc'] = False
            self.completedcalls['rfp'] = False
            print(e)
        
            
        return  booking_info


    def handle_cancellation(self, cancellation_info):

        return  cancellation_info

    def handle_flight_info(self,chat_session, booking_info):
        try :
            if booking_info.get("need-flights-data",'no').lower()  == 'no':
                self.completedcalls['nfd'] = False
            if booking_info.get("need-seat-data",'no').lower()  == 'no':
                self.completedcalls['ns'] = False
            if booking_info.get("need-flight-cost",'no').lower()  == 'no':
                self.completedcalls['nfc'] = False
            if booking_info.get("need-flights-data",'no').lower()  == 'yes' and not self.completedcalls['nfd']:
                nv = booking_info.get("need-flights-data",'').lower()
                if nv == self.completedcalls['need-new-flights-data'] :
                    return booking_info
                self.freeseats = None
                source = booking_info.get("source",None)
                destination = booking_info.get("destination",None)
                departure_date = booking_info.get("dateofdeparture",None)
                flight_data = "No flight for the source and destination on the routes on the day please ask the user for different dates"
                if source and destination and departure_date:
                    flight_data = get_flights(chat_session.collection_flight_dates,source,destination,departure_date)
                    if len(flight_data["flights"]) == 0:
                        flight_data = "No flight for the source and destination on the routes on the day please ask the user for different dates"
                    else:   
                        flight_data = json.dumps(flight_data)
                
                response = chat_session.chat.send_message("New Flights Data from admin :  " + flight_data)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                self.completedcalls['nfd'] = True
                return jres
        except:
            pass
        pass
    
        return  booking_info
    def handle_change_flight(self,chat_session, booking_info):
        try :

            if booking_info.get("need-flights-data",'no').lower()  == 'no':
                self.completedcalls['nfd'] = False
            if booking_info.get("need-seat-data",'no').lower()  == 'no':
                self.completedcalls['ns'] = False
            if booking_info.get("need-flight-cost",'no').lower()  == 'no':
                self.completedcalls['nfc'] = False
            if booking_info.get("readyforpayment",'no').lower()  == 'no':
                self.completedcalls['rfp'] = False

            if booking_info.get("readyforpayment",'no').lower()  == 'yes' and not self.completedcalls['rfp'] :
                print(booking_info)
                input_json = json.dumps(booking_info)
                booking_payload = create_booking_payload(input_json, user_data_json)
                print(booking_payload)
                result = chat_session.collection_flight_bookings.insert_one(booking_payload)
                
                response = chat_session.chat.send_message("from Admin : flight modification is completed share booking reference to user and thanks for using assitant and booking details are  :  " + json.dumps(booking_payload,cls=JSONEncoder) )
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                self.completedcalls['rfp'] = True


                booking_reference = booking_info.get("selected-booking-reference",'not-applicable')
                if booking_reference != 'not-applicable':
                    # delete a previous booking/ change the status to cancelled
                    # Find the booking by bookingReference and update bookingStatus
                    updated_booking = chat_session.collection_flight_bookings.find_one_and_update(
                        {"bookingReference": booking_reference},
                        {"$set": {"bookingStatus": "moved"}},
                        return_document=ReturnDocument.AFTER
                    )
                return jres 
            if booking_info.get("need-flight-cost",'no').lower()  == 'yes' and not self.completedcalls['nfc'] :
                
                            
                source = booking_info.get("source",None)
                destination = booking_info.get("destination",None)
                seat_number = booking_info.get("seat",None)
                seat_type = None
                if seat_number:
                    seat_type = classify_seat(seat_number)
                if source and destination and seat_type :
                    meal = booking_info.get("meal",None)
                    mealflag = False
                    if meal and meal !=  "not-applicable":
                        mealflag = True
                    fare, mealprice = get_flight_fare(source, destination, seat_type, mealflag)
                    


                    response = chat_session.chat.send_message("from Admin :new flight fare :  " + str(fare) + ", mealfare : " + str(mealprice) + " change fare : 650" + " mention refund from previous booking paid price if less than new total fare else ask for additional payment of the diference price if same fare mention 0 rupees and ask for payment confirmation"  )
                    response_message= ""
                    for c in response:
                        response_message += c.text
                    
                    extracted_json = extract_json_from_string(response_message)
                    jres = json.loads(extracted_json)
                    self.completedcalls['nfc'] = True
                    return jres
            if booking_info.get("need-seat-data",'no').lower()  == 'yes' and not self.completedcalls['ns'] :
                if not self.freeseats:
                    self.freeseats = generate_airplane_seats()
                seats = json.dumps(self.freeseats)

                
                response = chat_session.chat.send_message("unbooked Seats Data from admin :  " + seats)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                self.completedcalls['ns'] = True
                return jres
            
            if booking_info.get("need-flights-data",'no').lower()  == 'yes' and not self.completedcalls['nfd']:
                self.freeseats = None
                source = booking_info.get("source",None)
                destination = booking_info.get("destination",None)
                departure_date = booking_info.get("dateofdeparture",None)
                flight_data = "No flight for the source and destination on the routes on the day please ask the user for different dates"
                if source and destination and departure_date:
                    flight_data = get_flights(chat_session.collection_flight_dates,source,destination,departure_date)
                    if len(flight_data["flights"]) == 0:
                        flight_data = "No flight for the source and destination on the routes on the day please ask the user for different dates"
                    else:   
                        flight_data = json.dumps(flight_data)
                
                response = chat_session.chat.send_message("Flights Data from admin :  " + flight_data)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                self.completedcalls['nfd'] = True
                return jres
            
            
            print('rfp',booking_info.get("readyforpayment",'no').lower() )
            
        except Exception as e:
        
            self.completedcalls['nfd'] = False
            self.completedcalls['ns'] = False
            self.completedcalls['nfc'] = False
            self.completedcalls['rfp'] = False
            print(e)
        
            
        return  booking_info

    def handle_change_preferences(self, preferences_info):
        while not preferences_info['Name']:
            preferences_info['Name'] = input("What is your name for the preference change request? ")
        if preferences_info['flight_number'] == "not-applicable":
            preferences_info['flight_number'] = input("What is your flight number? ")
        if preferences_info['class'] == "not-applicable":
            preferences_info['class'] = input("What is your new class preference (economy/business)? ")
        if preferences_info['seat'] == "not-applicable":
            preferences_info['seat'] = input("What is your new seat preference? ")
        if preferences_info['meal'] == "not-applicable":
            preferences_info['meal'] = input("What is your meal preference? ")

        return {'intent': 'change_preferences', 'change_preferences': preferences_info}
