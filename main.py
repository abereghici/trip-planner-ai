from textwrap import dedent
from langchain_openai import ChatOpenAI
from crewai import Crew, Process

from dotenv import load_dotenv

from agents import TravelAgents
from tasks import TravelTasks

load_dotenv()

llm = ChatOpenAI(
    model="crewai-mistral",
    base_url="http://localhost:11434/v1",
    api_key="N/A"
)

class TripCrew: 
    def __init__(self, origin, destination, date_range, interests):
        self.origin = origin
        self.destination = destination
        self.date_range = date_range
        self.interests = interests

    def run(self): 
        agents = TravelAgents(origin, destination, date_range, interests)
        tasks = TravelTasks(origin, destination, date_range, interests)

        # Agents
        manager = agents.get_manager()
        travel_agent = agents.travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()
        quality_control_expert = agents.quality_control_expert()

        # Tasks
        manager_task = tasks.manager(manager)
        identify_city_task = tasks.identify_city(city_selection_expert)
        gather_city_info_task = tasks.gather_city_info(city_selection_expert)
        plan_itinerary_task = tasks.plan_itinerary(travel_agent)
        quality_control= tasks.quality_control(quality_control_expert,plan_itinerary_task)

        crew = Crew(
            agents=[
                manager,
                travel_agent,
                city_selection_expert,
                local_tour_guide,
                quality_control_expert],
            tasks=[manager_task,
                plan_itinerary_task,
                identify_city_task,
                gather_city_info_task,
                quality_control],
            process=Process.hierarchical,
            manager_llm=llm,
            verbose=2,
        )
        
        result = crew.kickoff()
        return result

if __name__ == '__main__':
    print("\n\n###########################")
    print("## Welcome to Trip Planner")
    print("###########################\n\n")
    origin = input(
        dedent("""From where will you be traveling from?
        """)
    )
    destination = input(
        dedent("""What is the city your are interested in visiting?
        """))

    date_range = input(
        dedent("""What is the date range you are interested in traveling?
        """))

    interests = input(
        dedent("""What are some of your high level interests or hobbies?
        """))

    trip_crew = TripCrew(origin, destination, date_range, interests)
    result = trip_crew.run()

    print("\n\n###########################")
    print("## Here is your trip plan")
    print("###########################\n\n")
    print(result)
