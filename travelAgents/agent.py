from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.genai import types
from google.adk.tools import ToolContext
from typing import Dict, Any
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

def save_route_to_state(
    tool_context: ToolContext,
    route: list[str]
) -> dict[str, str]:
    """Saves the list of selected route to state["routes"].

    Args:
        routes (list[str]): a list of strings representing the selected routes

    Returns:
        None
    """
    # Update the 'routes' key in the state with the new routes.
    # When the tool is run, ADK will create an event and make
    # corresponding updates in the session's state.
    existing_routes = tool_context.state.get("routes", [])
    tool_context.state["routes"] = route + existing_routes

    # A best practice for tools is to return a status message in a return dict
    return {"status": "success"}

def save_attractions_to_state(
    tool_context: ToolContext,
    attractions: list[str]
) -> dict[str, str]:
    """Saves the list of attractions to state["attractions"].

    Args:
        attractions [str]: a list of strings to add to the list of attractions

    Returns:
        None
    """
    # Load existing attractions from state. If none exist, start an empty list
    existing_attractions = tool_context.state.get("attractions", [])

    # Update the 'attractions' key with a combo of old and new lists.
    # When the tool is run, ADK will create an event and make
    # corresponding updates in the session's state.
    tool_context.state["attractions"] = existing_attractions + attractions

    # A best practice for tools is to return a status message in a return dict
    return {"status": "success"}

travel_route_planner = Agent(
    name="travel_route_planner",
    model="gemini-3.6-flash",
    description="Plan a travel route based on selected attractions.",
    instruction="""
        - Provide the user with a suggested travel route based on their selected attractions.
        - Provide options for them via air, train, or car or may they want to bike ride if available 
        - When they reply, use your tool to save their selected route
        and then provide more possible routes.
        - If they ask to view the list, provide a bulleted list of
        { routes? } and then suggest some more.
        """,
    tools=[save_route_to_state]
)

attractions_planner = Agent(
    name="attractions_planner",
    model="gemini-3.6-flash",
    description="Build a list of attractions to visit in a country.",
    instruction="""
        - Provide the user options for attractions to visit within their selected country.
        - When they reply, use your tool to save their selected attraction
        and then provide more possible attractions.
        - If user asks for route how to get to the attractions, send them to 'travel_route_planner'.
        - If they ask to view the list, provide a bulleted list of
        { attractions? } and then suggest some more.
        """,
    # before_model_callback=log_query_to_model,
    # after_model_callback=log_model_response,
    # When instructed to do so, paste the tools parameter below this line
    sub_agents=[travel_route_planner],
    tools=[save_attractions_to_state]
    )

travel_brainstormer = Agent(
    name="travel_brainstormer",
    model="gemini-3.6-flash",
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
    model="gemini-3.6-flash",
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