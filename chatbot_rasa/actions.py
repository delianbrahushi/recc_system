from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionApiInfo(Action):
    def name(self) -> Text:
        return "action_api_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_endpoint = "http://127.0.0.1:5000/api/documents"

        try:
            # Make a request to the Flask API
            response = requests.get(api_endpoint)

            if response.status_code == 200:
                # Extract the "documents" from the JSON response
                documents = response.json().get("documents", [])
                document_list = "\n".join(documents)

                # Send a message with the retrieved documents
                dispatcher.utter_message(text=f"\n{document_list}")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't fetch the document information at the moment. Please try again later.")

        except Exception as e:
            dispatcher.utter_message(text="An error occurred while fetching document information. Please try again later.")

        return []

class ActionApiInfo2(Action):
    last_event = None
    last_event_mentioned = False

    def name(self) -> Text:
        return "action_api_info_2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the user's intent
        intent = tracker.latest_message["intent"].get("name")

        if intent == "inquire_upcoming_events":
            if not self.last_event_mentioned:
                # Make a request to the Flask API only if the last event is not mentioned
                api_endpoint = "http://127.0.0.1:5000/api/events"

                try:
                    # Make a request to the Flask API
                    response = requests.get(api_endpoint)

                    if response.status_code == 200:
                        # Extract the "event" from the JSON response
                        event = response.json().get("event", {})
                        event_name = event.get("name", "Unknown Event")

                        # Store the last event
                        self.last_event = event

                        # Send a message with the retrieved event name
                        dispatcher.utter_message(text=f"The upcoming event is: {event_name}")
                    else:
                        dispatcher.utter_message(text="Sorry, I couldn't fetch the event information at the moment. Please try again later.")

                except Exception as e:
                    dispatcher.utter_message(text="An error occurred while fetching event information. Please try again later.")
            else:
                # If the last event is mentioned, use the stored event information
                event_name = self.last_event.get("name", "Unknown Event")
                dispatcher.utter_message(text=f"The upcoming event is: {event_name}")

            # Reset the flag for the next user turn
            self.last_event_mentioned = False

        elif intent == "inquire_event_details":
            # User is asking for event details
            if self.last_event:
                event_name = self.last_event.get("name", "Unknown Event")
                event_date = self.last_event.get("date", "Unknown Date")
                event_time = self.last_event.get("time", "Unknown Time")
                event_location = self.last_event.get("location", "Unknown Location")
                event_details = f"Event: {event_name}\nDate: {event_date}\nTime: {event_time}\nLocation: {event_location}"

                # Send a message with the retrieved event details
                dispatcher.utter_message(text=f"{event_details}")
            else:
                dispatcher.utter_message(text="No event details available. Please ask for upcoming events first.")

        return []

