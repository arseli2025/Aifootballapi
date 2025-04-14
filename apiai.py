import os
#from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from os import getenv
llm0 = ChatOpenAI(model="openai/gpt-4o-mini",
    api_key=getenv('openaikey'),
    base_url="https://openrouter.ai/api/v1")

prompt10=""" You are given the below API Documentation:
API documentation:
Base url to use for every call: https://v3.football.api-sports.io/
GET endpoints and parameters /standings
(/fixtures/lineups?fixture=Fixtureid) get lineups for one fixture or for a certain team in that fixture (/fixtures/lineups?fixture=Fixtureid&team=TEamID)
(/teams/statistics?season=season&team=teamid&league=league id)= the statistics of a team in relation to a given competition and season
(teams?league=leagueid&season=seasonid)=RETRIEVE ALL THE TEAMS FROM THE COMPETITION
(/players/squads?team=TEAMID)=current squad of a team.
(/players/topscorers?season=seasonid&league=leagueid)=top scorers for a league.
(/players/topassists?season=seasonid&league=leagueid)=players with most assists for a league.
(/players/topyellowcards?season=seasonid&league=leagueid)=players with most yellowcards for a league.
(/players/topredcards?season=seasonid&league=leagueid)=players with most redcards for a league.
(teams?search=teamname)= team id.
(leagues?search=country)= league id.
/fixtures?next=1 next match for one team.
2024 is current year to be used ONLY in dates, from and to.
///
(/fixtures/players?fixture=fixtureid)=Get the players statistics from one fixture.
/players?id=playerid&season=season Get players statistics for a season
Use this url https://v2.api-football.com/players/search/(player last name ONLY) use v2 only to get the id when searching for a player only for this purpose use that url or get player id.
(/transfers?player=playerid) Get all available transfers a player use v3 url
(/coachs?search=last name of coach) = when searching for a coach only for this purpose use that url or get coach id use v3 url
Get all available trophies for a player or a coach. /trophies?player=playerid or /trophies?coach=coachid
(/predictions?fixture=fixtureid) get prediction for a certain fixture id
(/fixtures/events?fixture=fixtureid)=Get the events from a fixture. use team parameter too for a team id.
(/odds?season=season&fixture=fixtureid)=odds for a fixture ALWAYS  GET odds after after getting predictions parameter, use 2024 season if not specified.
This API is for getting the standings  football(Soccer) data.ONLY GIVE URL.
wHATEVER QUESTION YOU ARE ASKED,Use search parameters (teams?search=teamname)= team id (leagues?search=country)= league id, first to find league or team FIRST .FIND THE TEAM IDS FIRST AS YOU NOT KNOW THEM AT ALL.DO NOT MAKE UP TEAM IDS.you know nothing. USE requests to call the api url one by one TOOL ONE BY ONE URL.
Give predictions info too if odds are asked."""




from langchain_core.prompts import ChatPromptTemplate

promptano = ChatPromptTemplate.from_messages([
    ("system", prompt10+" "+ "Respond to the human as helpfully and accurately as possible. You have access to the following tools:\n\n{tools}\n\nUse a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).\n\nValid \"action\" values: \"Final Answer\" or {tool_names}\n\nProvide only ONE action per $JSON_BLOB, as shown:\n\n```\n{{\n  \"action\": $TOOL_NAME,\n  \"action_input\": $INPUT\n}}\n```\n\nFollow this format:\n\nQuestion: input question to answer\nThought: consider previous and subsequent steps\nAction:\n```\n$JSON_BLOB\n```\nObservation: action result\n... (repeat Thought/Action/Observation N times)\nThought: I know what to respond\nAction:\n```\n{{\n  \"action\": \"Final Answer\",\n  \"action_input\": \"Final response to human\"\n}}\n\nBegin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}\n\n{agent_scratchpad}\n (reminder to respond in a JSON blob no matter what)"),
])

from langchain.agents import AgentExecutor,create_structured_chat_agent
from langchain_core.tools import tool
import requests
import os
os.environ['football_BEARER_TOKEN'] = getenv('football_BEARER_TOKEN')
headers = {"x-rapidapi-key":f"{os.environ['football_BEARER_TOKEN']}"}
@tool
def requests(url: str):
    """Making get requests to api and summarize the response"""
    import os
    os.environ['football_BEARER_TOKEN'] = getenv('football_BEARER_TOKEN')
    headers = {"x-rapidapi-key":f"{os.environ['football_BEARER_TOKEN']}"}
    import requests
    kari=requests.get(url,headers=headers)
    return str(kari.text)
  
tools = [requests]

agent = create_structured_chat_agent(llm0, tools, promptano)
def gari(prompt):
    agent1 = AgentExecutor(
    agent=agent, tools=tools, verbose=False,handle_parsing_errors=True)
    faro=agent1.invoke({"input": prompt})
    return faro['output']
from flask import Flask, request, jsonify
from waitress import serve
app = Flask(__name__)    
@app.route('/process', methods=['POST'])
def process():
    # Get the raw data from the request body
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Process the data using the defined function
    processed_data = gari(data)
    
    # Return the processed data in the response
    return jsonify({'processed_data': processed_data})

if __name__ == '__main__':
     serve(app, host='0.0.0.0', port=7860,threads=5)