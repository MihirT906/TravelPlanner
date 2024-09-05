from crewai import Crew
from textwrap import dedent
from agents import TravelAgents
from tasks import TravelTasks
import streamlit as st
import os

from dotenv import load_dotenv
load_dotenv()


class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TravelAgents()
        tasks = TravelTasks()

        # Define your custom agents and tasks here
        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()

        # Custom tasks include agent name and variables as input
        plan_itinerary = tasks.plan_itinerary(
            expert_travel_agent,
            self.cities,
            self.date_range,
            self.interests
        )

        identify_city = tasks.identify_city(
            city_selection_expert,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )

        gather_city_info = tasks.gather_city_info(
            local_tour_guide,
            self.cities,
            self.date_range,
            self.interests
        )

        # Define your custom crew here
        crew = Crew(
            agents=[expert_travel_agent,
                    city_selection_expert,
                    local_tour_guide
                    ],
            tasks=[
                plan_itinerary,
                identify_city,
                gather_city_info
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# Streamlit App
st.title("Trip Planner Crew")

# Input fields
origin = st.text_input("From where will you be traveling from?")
cities = st.text_input("What are the cities options you are interested in visiting?")
date_range = st.date_input("What is the date range you are interested in traveling?")
interests = st.text_input("What are some of your high-level interests and hobbies?")

# Generate trip plan when the button is clicked
if st.button("Generate Trip Plan"):
    if origin and cities and date_range and interests:
        # Instantiate TripCrew and run it
        trip_crew = TripCrew(origin, cities, date_range, interests)
        result = trip_crew.run()

        # Save the result to a file
        with open("trip_plan.txt", "w") as file:
            file.write(result)

        st.success("Trip plan has been generated and saved to 'trip_plan.txt'!")

    # Check if the file exists and display its contents
    if os.path.exists("trip_plan.txt"):
        with open("trip_plan.txt", "r") as file:
            trip_plan = file.read()
            st.markdown(f"### Here is your Trip Plan:\n{trip_plan}")
    else:
        st.warning("No trip plan found. Please provide inputs to generate a trip plan.")
