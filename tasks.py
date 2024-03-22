from crewai import Task
from textwrap import dedent

class TravelTasks:
    def __init__(self, origin, destination, date_range, interests):
        self.origin = origin
        self.destination = destination
        self.date_range = date_range
        self.interests = interests

    def manager(self, agent):
        return Task(
            description=dedent(f"""
        Oversee the integration of research findings, trip suggestions, 
        and quality control feedback to produce a 7-day travel itinerary
        specifically tailored to the user's interests: {self.interests} and 
        their travel destination: {self.destination}. The final output should be 
        a comprehensive with detailed per-day plans, including budget, 
        packing suggestions."""),
            agent=agent,
            async_execution=False
        )
    
    def identify_city(self, agent):
        return Task(
            description=dedent(f"""
                Analyze and select the best city for the trip based 
                on specific criteria such as weather patterns, seasonal
                events, and travel costs. This task involves comparing
                multiple cities, considering factors like current weather
                conditions, upcoming cultural or seasonal events, and
                overall travel expenses. 
                                                
                Make sure you stay inside the country that the user requests.
                
                Your final answer must be a detailed
                report on the chosen city, and everything you found out
                about it, including the actual flight costs, weather 
                forecast and attractions.

                Traveling from: {self.origin}
                Traveling to: {self.destination}
                Trip Date: {self.date_range}
                Traveler Interests: {self.interests}
                """),
            agent=agent,
            expected_output=dedent(f"""
                A detailed report on the selected city including:
                - Justification for city selection based on weather, seasonal events, and prices
                - Overview of flight costs, weather forecast, and main attractions
                - Analysis comparing multiple cities and why the chosen city is best for the trip
            """),
            async_execution=False
        )
    
    def gather_city_info(self, agent):
        return Task(
            description=dedent(f"""
                As a local expert on this city you must compile an 
                in-depth guide for someone traveling there and wanting 
                to have THE BEST trip ever!
                Gather information about  key attractions, local customs,
                special events, and daily activity recommendations.
                Find the best spots to go to, the kind of place only a
                local would know.
                This guide should provide a thorough overview of what 
                the city has to offer, including hidden gems, cultural
                hotspots, must-visit landmarks, weather forecasts, and
                high level costs.
                                            
                Make sure you only offer suggestions inside of the country.
                
                The final answer must be a comprehensive city guide, 
                rich in cultural insights and practical tips, 
                tailored to enhance the travel experience.

                Trip Date: {self.date_range}
                Traveling to: {self.destination}
                Traveler Interests: {self.interests}
                """),
            agent=agent,
            expected_output=dedent(f"""
                An in-depth city guide featuring:
                - Key attractions and local customs
                - Special events happening around the trip dates
                - Recommendations for daily activities including hidden gems and cultural hotspots
                - Weather forecast for the trip dates with appropriate clothing suggestions
                - High-level cost estimates for suggested activities and spots
                """),
            async_execution=False
        )
    
    def plan_itinerary(self, agent):
        return Task(
        description=dedent(f"""
            Expand research into a a full 7-day travel 
            itinerary with detailed per-day plans, including 
            weather forecasts, places to eat, packing suggestions, 
            and a budget breakdown.
                                        
            Make sure that you only offer suggestions inside of the
            country that the user requests.
            
            You MUST suggest actual places to visit, actual hotels 
            to stay and actual restaurants to go to.
            
            This itinerary should cover all aspects of the trip, 
            from arrival to departure, integrating the city guide
            information with practical travel logistics.
            
            Your final answer MUST be a complete expanded travel plan,
            formatted as markdown, encompassing a daily schedule,
            anticipated weather conditions, recommended clothing and
            items to pack, and a detailed budget, ensuring THE BEST
            TRIP EVER, Be specific and give it a reason why you picked
            # up each place, what make them special!

            Trip Date: {self.date_range}
            Traveling from: {self.origin}
            Traveling to: {self.destination}
            Traveler Interests: {self.interests}
        """),
        agent=agent,
        expected_output=dedent(f"""
            A complete 7-day travel itinerary in markdown format to {self.destination}
            """),
        async_execution=False,
    )
    
    def quality_control(self, agent, context):
        return Task(
    description=dedent(f"""
        Look over the 7-day travel itinerary and provide feedback
        on the quality of the plan and to make sure that the 
        itinerary follows the same format as the following 7 day 
        example where you outline what the traveler will do in the 
        morning, afternoon, and evening along with optional opportunities. 
        Obviously the exact information will differ for each trip, 
        but the format should be the same. 
        
        Your feedback should only include suggestions around formatting 
        and making sure the itenerary includes all of the necessary 
        information to generate the following itinerary. If the itinerary 
        is missing any information, you should provide feedback on what is 
        missing and how it can be improved. 
                       
        If the itinerary includes any information that is not necessary, 
        provide feedback on what needs to be removed and why.
                
                       
        EXAMPLE 7 DAY ITNERARY:
                       
        **Day 1: Arrival in Bangkok**
        - Arrival at Suvarnabhumi Airport, transfer to Nasa Vegas Hotel.
        - Lunch at a local restaurant.
        - Visit the Grand Palace and Wat Phra Kaew ($10).
        - Dinner at Thip Samai Pad Thai.
        - Drinks at Sky Bar.

        **Day 2: Bangkok**
        - Breakfast at the hotel.
        - Visit Wat Arun ($3) and explore the local market.
        - Lunch at Or Tor Kor Market.
        - Evening visit to Asiatique The Riverfront.
        - Dinner at Jok Pochana.
        - Nightlife at RCA (Royal City Avenue).

        **Day 3: Bangkok to Krabi**
        - Breakfast at the hotel and check out.
        - Flight to Krabi ($100) and check-in at Sea Seeker Krabi Resort.
        - Visit to Krabi Town and local markets.
        - Dinner at Chalita Cafe & Restaurant.
        - Nightlife at Ao Nang Center Point.

        **Day 4: Krabi**
        - Breakfast at the hotel.
        - Full-day tour of the Four Islands (Phra Nang Cave Beach, Chicken Island, Tup Island, and Poda Island) ($20).
        - Lunch on the tour.
        - Return to the resort.
        - Dinner at Jenna's Bistro & Wine.
        - Nightlife at Boogie Bar.

        **Day 5: Krabi**
        - Breakfast at the hotel.
        - Hike to the Tiger Cave Temple.
        - Lunch at Krua Thara Seafood Restaurant.
        - Visit to Emerald Pool and Hot Springs ($10).
        - Dinner at Nong Bua Seafood.
        - Nightlife at Carlito's Bar.

        **Day 6: Krabi to Bangkok**
        - Breakfast at the hotel and check out.
        - Flight back to Bangkok ($100) and check-in at Nasa Vegas Hotel.
        - Visit Chatuchak Weekend Market.
        - Dinner at Som Tam Nua.
        - Nightlife at Soi Cowboy.

        **Day 7: Bangkok**
        - Breakfast at the hotel.
        - Visit to the Floating Market.
        - Lunch at Pier 21 Food Terminal.
        - Participate in the Loy Krathong Festival.
        - Farewell dinner at Sirocco & Sky Bar.

        **Budget Breakdown:**
        - Accommodation: $490 (7 nights at $70/night)
        - Meals: $210 (21 meals at $10/meal)
        - Public Transportation: $210 (7 days at $30/day)
        - Flights (Bangkok to Krabi round-trip): $200
        - Activities: $200
        - Total: $1310

        **Packing Suggestions:**
        - Lightweight clothing due to warm weather
        - Rain jacket or umbrella for unexpected showers
        - Swimwear for beach activities
        - Hiking shoes for treks
        - Formal attire for nightlife
    """),
        agent=agent,
        context=[context],
        expected_output=dedent(f"""
            Actionable feedback on the 7-day travel itinerary with 
            assessment of the itinerary's adherence to the format and quality standards
            """),
        async_execution=False
    )
