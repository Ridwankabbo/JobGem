from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic import hub
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import HarmBlockThreshold, HarmCategory
from django.conf import settings
from .ai_tools import search_jobs, applay_job

def run_agent(user_querry, histroy_list=[]):
    llm = ChatGoogleGenerativeAI(
        model = 'Gemini-2.5-flash',
        temperature = 0, 
        google_api_key = settings.GEMINI_API_KEY,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
    
    tools = [search_jobs, applay_job]
    
    instructions = """ 
        You are a Banglay job ai assinstant.
        If you find jobs to show, your 'Final Answer' must follow this EXACT structure:

        MESSAGE: [A friendly response in Bengali about the items found]
        DATA: [A JSON array of product objects with: "id", "title","requirements", "location", "experieance", "deadline"]

        If no jobs are found or it's a general question, just provide the MESSAGE.
    """
    
    template = """Answer the following questions as best you can. You have access to the following tools:

        {tools}
        
        Use the following format:

        Question: the input question you must answer 
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        """ + instructions + """
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}
    """
    
    prompt = PromptTemplate.from_template(template)
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbos=True,
        handle_parsing_errors=True,
        
    )
    
    result = agent_executor.invoke({'input': user_querry})
    return result['output']