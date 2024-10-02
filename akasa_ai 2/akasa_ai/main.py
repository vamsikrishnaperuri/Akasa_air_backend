import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime
from helpers import *
from prompts import *
from models import *
from fastapi.middleware.cors import CORSMiddleware
from fares import *
# Import all the necessary packages
import google.generativeai as genai

import os
import time


# keys 
API_KEY = "AIzaSyARnPqvmSD8A-dXq1NQ1DjG2n2CjwAN5nw"


# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# booking code



# MongoDB connection details
client = MongoClient('mongodb+srv://root:my^7#kj@cluster0.9podb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['flight_booking_db']
collection_flight_bookings = db['flight_bookings']
collection_flight_dates = db['flight_dates']




genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

from typing import List


class ChatSession:
    def __init__(self):
        self.conversation_history = []
        self.fbs_manager = FlightBookingSystem()
        self.collection_flight_dates = collection_flight_dates
        self.collection_flight_bookings = collection_flight_bookings


        # The runner program to convert queries to json

    def new_ses(self):
        self.intent = "new"
        self.conversation_history = []
        self.chat = model.start_chat(history=self.conversation_history)
    def clear_ses(self):
        self.conversation_history = []
        self.chat = model.start_chat(history=self.conversation_history)

    def getdate(self):
        # Get the current date
        current_date = datetime.now()

        # Format the date to DD/MM/YYYY
        formatted_date = current_date.strftime("%d/%m/%Y")
        return formatted_date



    def clear_history(self):
        self.conversation_history = []

    def add_message(self, user_message: str = None):
        try :
            if not user_message:
                context = get_f1_context(self.getdate(),'Delhi')
                self.fbs_manager.reset()
                self.intent = "new"
                # print(context)
                response = self.chat.send_message(context)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                if "general" in jres:
                    self.conversation_history.append({"user": "ai","msg": {"response": jres["general"]['response'] }}) 
                else :
                    response1 = """Hello! I am Akasa Air's AI assistant. I can help you with booking, cancelling, checking flight information, changing flights, and changing your preferences. What can I help you with today?"""

                    self.conversation_history.append({"user": "ai", "msg": {"response": response1 }})
                return
            if user_message and self.intent == "new":
                self.fbs_manager.freeseats = None
                response = self.chat.send_message("user query : " + user_message)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                if "general" in jres:
                    self.conversation_history.append({"user": "ai", "msg": {"response": jres["general"]['response'] }}) 
                    return
                # print(jres)
                self.intent, json_res = self.fbs_manager.classify_intent(ai_res=jres)
                print(self.intent)

                self.clear_ses()
                if self.intent == "booking":
                    booking_context = get_booking_context(self.getdate(),"Delhi",json_res)
                    response = self.chat.send_message(booking_context)
                    response_message= ""
                    for c in response:
                        response_message += c.text
                    
                    extracted_json = extract_json_from_string(response_message)
                    jres = json.loads(extracted_json)
                    self.conversation_history.append({"user": "ai", "msg": jres})
                    return
                if self.intent == "cancelling":
                    #print("Intent is Cancelling")
                    bookings = get_bookings_f("harshasrikasyap807@gmail.com",collection_flight_bookings)
                    print(bookings)
                    cancelling_context = get_cancelling_context(self.getdate(),"Delhi",bookings)
                    response = self.chat.send_message(cancelling_context)
                    response_message= ""
                    for c in response:
                        response_message += c.text
                    
                    extracted_json = extract_json_from_string(response_message)
                    jres = json.loads(extracted_json)
                    self.conversation_history.append({"user": "ai", "msg": jres})
                    return
                if self.intent == "change_flight":
                    bookings = get_bookings_f("harshasrikasyap807@gmail.com",collection_flight_bookings)
                    change_booking_context = get_change_booking_context(self.getdate(),"Delhi",bookings)
                    response = self.chat.send_message(change_booking_context)
                    response_message= ""
                    for c in response:
                        response_message += c.text
                    
                    extracted_json = extract_json_from_string(response_message)
                    jres = json.loads(extracted_json)
                    self.conversation_history.append({"user": "ai", "msg": jres})
                    return
                if self.intent == "flight_info":
                    change_booking_context = get_flight_info_context(self.getdate(),"Delhi","")
                    response = self.chat.send_message(change_booking_context)
                    response_message= ""
                    for c in response:
                        response_message += c.text
                    
                    extracted_json = extract_json_from_string(response_message)
                    jres = json.loads(extracted_json)
                    self.conversation_history.append({"user": "ai", "msg": jres})
                    return
                    
                
                
                self.conversation_history.append({"user": "ai", "msg": self.intent + "feature under development"})
                return
            # self.fbs_manager.handle_intent()
            if self.intent == "booking":
                response = self.chat.send_message("user query : " + user_message)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                njres = self.fbs_manager.handle_booking(self , jres)
                self.conversation_history.append({"user": "ai", "msg": njres})
                return
            if self.intent == "change_flight":
                response = self.chat.send_message("user query : " + user_message)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                njres = self.fbs_manager.handle_change_flight(self , jres)
                self.conversation_history.append({"user": "ai", "msg": njres})
                return
            if self.intent == "flight_info":
                response = self.chat.send_message("user query : " + user_message)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                njres = self.fbs_manager.handle_flight_info(self , jres)
                self.conversation_history.append({"user": "ai", "msg": njres})
                return
            if self.intent == "cancelling":
                # This intent is for cancelling
                response = self.chat.send_message("user_query : "+user_message)
                response_message= ""
                for c in response:
                    response_message += c.text
                
                extracted_json = extract_json_from_string(response_message)
                jres = json.loads(extracted_json)
                self.conversation_history.append({"user": "ai", "msg":jres})
                yescancel =  jres.get("go-for-cancel", "no")
                selectedBf = jres.get('selected-booking-reference', None)
                if yescancel == 'yes':
                    # Update the database to change it to cancelled
                    if selectedBf:
                        filter_criteria = { 
                            "passengerDetails.contactDetails.email": "harshasrikasyap807@gmail.com",
                            "bookingReference": selectedBf
                        }

                        # Define the update operation
                        update_operation = { "$set": { "bookingStatus": "Cancelled" } }
                        result = collection_flight_bookings.update_one(filter_criteria, update_operation)
                        jres['bookingStatus'] = "Cancelled"
                        print("Result of db-ops : ", result)
                
                return jres
        except Exception as e:
            print(e)
            time.sleep(5)
            return self.add_message( user_message)
            

    def get_history(self):
        return self.conversation_history

# Initialize a global chat session (for simplicity)
chat_session = ChatSession()


class UserMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(user_message: UserMessage):
    # Simulate a response (this can be replaced by any response-generating logic, like an AI model)
    if len(chat_session.conversation_history) == 0 or user_message.message.lower() == "new" or user_message.message.lower() == "":
        # set the flow to f1
        chat_session.clear_history()
        chat_session.new_ses()


        # The runner program to convert queries to json

        chat_session.add_message()

        return {"history": chat_session.get_history()}

    # # Add the new message and response to the chat history
    chat_session.add_message(user_message.message)

    # Return the current conversation history
    return {"history": chat_session.get_history()}






# Pydantic model for booking data
class PassengerDetails(BaseModel):
    firstName: str
    lastName: str
    dateOfBirth: datetime
    passportNumber: str
    nationality: str
    contactDetails: dict

class FlightDetails(BaseModel):
    flightNumber: str
    airline: str
    departure: dict
    arrival: dict
    flightClass: str
    seatNumber: Optional[str] = None

class PaymentDetails(BaseModel):
    amount: float
    currency: str
    paymentMethod: str
    paymentStatus: str
    paymentDate: datetime

class LoyaltyProgram(BaseModel):
    programName: Optional[str] = None
    membershipNumber: Optional[str] = None
    pointsEarned: Optional[int] = 0

class Booking(BaseModel):
    bookingReference: str
    passengerDetails: PassengerDetails
    flightDetails: FlightDetails
    bookingStatus: str
    paymentDetails: PaymentDetails
    specialRequests: Optional[str] = None
    loyaltyProgram: Optional[LoyaltyProgram] = None
    createdAt: datetime
    updatedAt: datetime

# Endpoint to save a new booking
@app.post("/bookings/")
async def save_booking(booking: Booking):
    # Convert booking to a dictionary and insert into MongoDB
    booking_dict = booking.dict()
    result = collection_flight_bookings.insert_one(booking_dict)
    return {"booking_id": str(result.inserted_id), "message": "Booking saved successfully"}

# Endpoint to get bookings by email or phone
@app.get("/bookings/")
async def get_bookings(email: Optional[str] = None, phone: Optional[str] = None):
    if not email and not phone:
        raise HTTPException(status_code=400, detail="Email or phone number is required")
    
    query = {}
    if email:
        query['passengerDetails.contactDetails.email'] = email
    if phone:
        query['passengerDetails.contactDetails.phone'] = phone

    bookings = list(collection_flight_bookings.find(query))

    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for the given criteria")

    # Convert ObjectId to string
    for booking in bookings:
        booking["_id"] = str(booking["_id"])

    return bookings




# passenger user profile routes

collection_user_profiles = db['user_profiles']



# Pydantic models for user data
class VisitedCity(BaseModel):
    city_code: str
    city_name: str
    visit_count: int

class PreferredSeat(BaseModel):
    seat: str
    booking_count: int

class PreferredDepartureTime(BaseModel):
    start: str
    end: str

class FoodPreference(BaseModel):
    item: str
    selection_count: int

class FlightDuration(BaseModel):
    count: int
    time_range: str

class FlightDurations(BaseModel):
    morning: FlightDuration
    noon: FlightDuration
    evening: FlightDuration
    midnight: FlightDuration

class UserProfile(BaseModel):
    name: str
    date_of_birth: datetime
    home_city: str
    home_airport_code: str
    most_preferred_class: str
    visited_cities: List[VisitedCity]
    preferred_seats: List[PreferredSeat]
    preferred_departure_time: PreferredDepartureTime
    food_preferences: List[FoodPreference]
    flight_durations: FlightDurations
    joined_akasa: str
    email: Optional[str] = None
    phone: Optional[str] = None

# Endpoint to insert user profile
@app.post("/users/")
async def create_user_profile(user_profile: UserProfile):
    # Check if email or phone exists for the user
    if not user_profile.email and not user_profile.phone:
        raise HTTPException(status_code=400, detail="Email or phone number is required.")
    
    # Ensure there isn't an existing user with the same email or phone
    existing_user = collection_user_profiles.find_one({"$or": [{"email": user_profile.email}, {"phone": user_profile.phone}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="A user with this email or phone number already exists.")
    
    user_profile_dict = user_profile.dict()
    result = collection_user_profiles.insert_one(user_profile_dict)
    
    return {"user_id": str(result.inserted_id), "message": "User profile created successfully"}

# Endpoint to get user profile by email or phone
@app.get("/users/")
async def get_user_profile(email: Optional[str] = None, phone: Optional[str] = None):
    if not email and not phone:
        raise HTTPException(status_code=400, detail="Email or phone number is required.")
    
    query = {}
    if email:
        query['email'] = email
    if phone:
        query['phone'] = phone

    user = collection_user_profiles.find_one(query)

    if not user:
        raise HTTPException(status_code=404, detail="User profile not found.")
    
    user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
    return user

# Endpoint to update user profile by email or phone
@app.put("/users/")
async def update_user_profile(email: Optional[str] = None, phone: Optional[str] = None, updated_data: UserProfile = None):
    if not email and not phone:
        raise HTTPException(status_code=400, detail="Email or phone number is required.")

    query = {}
    if email:
        query['email'] = email
    if phone:
        query['phone'] = phone

    # Check if user exists
    existing_user = collection_user_profiles.find_one(query)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User profile not found.")
    
    # Convert the Pydantic object to a dictionary
    updated_data_dict = updated_data.dict(exclude_unset=True)

    # Update the user profile
    result = collection_user_profiles.update_one(query, {"$set": updated_data_dict})

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes were made to the user profile.")

    return {"message": "User profile updated successfully"}






#flights inof


@app.get("/health")
def health ():
    return {"status" :"200" }


@app.get("/flights/")
def get_flights(source: str, destination: str, departure_date: str):
    try:
        departure_date_cleaned = departure_date.strip()
        departure_date_obj = datetime.strptime(departure_date_cleaned, '%d/%m/%Y')
        day_of_week_str = departure_date_obj.strftime('%A')

        # Log the input parameters and computed values
        print(f"Requesting flights with source: {source}, destination: {destination}, departure_date: {departure_date_cleaned}")
        print(f"Computed day_of_week: {day_of_week_str}")

        # Prepare the query
        query = {
            "origin": source,
            "destination": destination,
            "validFrom": {"$gte": departure_date_obj.strftime('%d/%m/%Y')},
            # "validTo": {"$gte": departure_date_obj.strftime('%d/%m/%Y')}
        }

        print(f"Query criteria: {query}")

        flights = list(collection_flight_dates.find(query))
        print("Fetched flights:", flights)

        valid_flights = [
            flight for flight in flights if day_of_week_str in flight['dayOfWeek'].split(',')
        ]
        print("Valid flights after filtering:", valid_flights)

        sorted_flights = sorted(valid_flights, key=lambda x: datetime.strptime(x['scheduledDepartureTime'], '%H:%M:%S'))

        result = [{
            "flightNumber": flight['flightNumber'],
            "airline": flight['airline'],
            "departureTime": flight['scheduledDepartureTime'],
            "arrivalTime": flight['scheduledArrivalTime'],
            "origin": flight['origin'],
            "destination": flight['destination'],
        } for flight in sorted_flights]

        return {"flights": result, 'day_of_week': day_of_week_str}

    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}
# html all other routes



# Mount static directory for Flutter web app (similar to Flask's static folder)
app.mount("/static", StaticFiles(directory="static/web"), name="static")

# Set up Jinja2Templates for rendering HTML files
templates = Jinja2Templates(directory="static/web")

# Route to serve the index.html when accessing "/web/"
@app.get("/web/")
async def render_page_web(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Dynamic route to serve files from the Flutter web app directory (/web/<filename>)
@app.get("/web/{name:path}")
async def return_flutter_doc(name: str):
    file_path = os.path.join("static/web", name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}

# Root route to render the index.html file ("/")
@app.get("/")
async def render_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Catch-all route to handle any other file requests ("/<filename>")
@app.get("/{name:path}")
async def return_flutter_doc_root(name: str):
    file_path = os.path.join("static/web", name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}




# Entry point for running the FastAPI app
def main():
    import uvicorn
    port = int(os.environ.get('PORT', 80))  # Default to port 80 if no env variable is set
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()