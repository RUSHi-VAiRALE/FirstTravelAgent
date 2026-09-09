from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.genai import types
# def get_current_time(city: str) -> dict:
#     """Returns the current time in a specified city."""
#     return {"status": "success", "city": city, "time": "10:30 AM"}


# google_search = GoogleSearchTool()

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='Searches public developer sources for information.',
#     instruction="""
#     You are the Web Search Agent.
#     Your task is to search public developer sources (e.g. GitHub issues, StackOverflow, official documentation) using Google Search.
#     Provide a clear summary of public patched workarounds or documentation.
#     Don't provide long info just provide a summary of the public patched workarounds or documentation.
#     Please include the source of the information in your summary.
#     """,
#     tools=[google_search],
# )

attractions_planner = Agent(
    name="attractions_planner",
    model="gemini-2.5-flash",
    description="Build a list of attractions to visit in a country.",
    instruction="""
        - Provide the user options for attractions to visit within their selected country.
        """,
    # before_model_callback=log_query_to_model,
    # after_model_callback=log_model_response,
    # When instructed to do so, paste the tools parameter below this line

    )

travel_brainstormer = Agent(
    name="travel_brainstormer",
    model="gemini-2.5-flash",
    description="Help a user decide what country to visit.",
    instruction="""
        Provide a few suggestions of popular countries for travelers.
        
        Help a user identify their primary goals of travel:
        adventure, leisure, learning, shopping, or viewing art

        Identify countries that would make great destinations
        based on their priorities.
        """,
    # before_model_callback=log_query_to_model,
    #after_model_callback=log_model_response,
    )

root_agent = Agent(
    name="steering",
    model="gemini-2.5-flash",
    description="Start a user on a travel adventure.",
    instruction="""
        Ask the user if they know where they'd like to travel
        or if they need some help deciding.
        If they need help deciding, send them to
        'travel_brainstormer'.
        If they know what country they'd like to visit,
        send them to the 'attractions_planner'.
        """,
    generate_content_config=types.GenerateContentConfig(
        temperature=1.5,
    ),
    # Add the sub_agents parameter when instructed below this line
    sub_agents=[travel_brainstormer, attractions_planner]
)