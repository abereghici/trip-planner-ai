from textwrap import dedent
from crewai import Agent
from langchain.agents import load_tools
from langchain_community.tools import DuckDuckGoSearchRun

from tools.calculator_tools import CalculatorTools
from tools.content_tools import ContentTools

search_tool = DuckDuckGoSearchRun()
human_tools = load_tools(["human"])

class TravelAgents:
    def __init__(self, origin, destination, date_range, interests):
        self.origin = origin
        self.destination = destination
        self.date_range = date_range
        self.interests = interests

    def get_manager(self):
        return Agent(
            role="Travel Manager",
            goal=dedent(f"""Coordinate the trip to {self.destination} ensure a seamless integration of research findings into 
        a comprehensive travel report with daily activities, budget breakdown, 
        and packing suggestions."""),
            backstory="""With a strategic mindset and a knack for leadership, you excel 
    at guiding teams towardstheir goals, ensuring the trip not only meets but exceed 
    expectations. You also validate your final output before presenting it to the client.""",
            verbose=True,
            allow_delegation=True,
        )

    def travel_agent(self):
        return Agent(
            role='Travel Agent',
            goal=dedent(f"""Create the most amazing travel itineraries with budget and 
        packing suggestions for your clients to travel to {self.destination}."""),
            verbose=True,
            backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
            tools=[CalculatorTools().calculate],
            max_iter=7
        )

    def city_selection_expert(self):
        return Agent(
            role='City Selection Expert',
            goal='Select the best city based on weather, season, and prices',
            verbose=True,
            backstory="""An expert in analyzing travel data to pick ideal destinations""",
            tools=[search_tool, ContentTools().read_content],
        )

    def local_tour_guide(self):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            verbose=True,
            backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
            tools=[search_tool, ContentTools().read_content],
        )

    def quality_control_expert(self):
        return Agent(
            role='Quality Control Expert',
            goal="""Ensure every travel itinerary and report meets the highest 
        standards of quality, accuracy, and client satisfaction. 
        Review travel plans for logistical feasibility, budget adherence, 
        and overall quality, making necessary adjustments to elevate 
        the client's experience. Act as the final checkpoint before plans are 
        presented to the client, ensuring all details align with the agency's 
        reputation for excellence.""",
            verbose=True,
            backstory="""With a meticulous eye for detail and a passion for excellence, 
        you have built a career in ensuring the highest standards in travel 
        planning and execution. Your experience spans several years within the 
        travel industry, where you have honed your skills in quality assurance,
          client service, and problem-solving. Known for your critical eye and 
          commitment to excellence, you ensure that no detail, no matter 
          how small, is overlooked. Your expertise not only lies in identifying 
          areas for improvement but also in implementing solutions that enhance 
          the overall client experience. Your role as a quality control expert 
          is the culmination of your dedication to elevating travel experiences 
          through precision, reliability, and client satisfaction.""",
            tools=[]+human_tools,
        )
