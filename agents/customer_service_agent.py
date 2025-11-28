"""Customer Service Agent - Ticket handling and case management"""
from typing import List, Dict
from langchain.tools import Tool, StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.prebuilt import create_react_agent
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from config.ai_core_config import AICorConfig, set_environment_variables

set_environment_variables()

class TicketInput(BaseModel):
    ticket_text: str = Field(description="Support ticket text to analyze")

class CustomerServiceAgent:
    """AI Agent for Customer Service Operations"""
    
    def __init__(self, deployment_id: str = None):
        self.deployment_id = deployment_id or AICorConfig.LLM_DEPLOYMENT_ID
        self.llm = ChatOpenAI(deployment_id=self.deployment_id, temperature=0.1)
        self.tools = self._load_tools()
        self.agent = create_react_agent(self.llm, self.tools)
    
    @property
    def agent_name(self) -> str:
        return "Customer Service Agent"
    
    def _load_tools(self) -> List:
        def classify_ticket(ticket_text: str) -> Dict:
            categories = {"billing": ["invoice", "payment"], "technical": ["error", "bug"]}
            ticket_lower = ticket_text.lower()
            detected = "general"
            for cat, keywords in categories.items():
                if any(kw in ticket_lower for kw in keywords):
                    detected = cat
                    break
            return {"category": detected, "priority": "medium", "confidence": 0.87}
        
        def search_knowledge_base(query: str) -> List[Dict]:
            return [{"id": "KB001", "title": "How to process refunds", "relevance": 0.92}]
        
        def recommend_action(case_summary: str) -> Dict:
            return {"action": "Schedule callback", "confidence": 0.89}
        
        return [
            StructuredTool.from_function(func=classify_ticket, name="classify_ticket",
                description="Classify support ticket", args_schema=TicketInput),
            Tool(name="search_kb", func=search_knowledge_base, description="Search KB"),
            Tool(name="recommend_action", func=recommend_action, description="Get next action"),
        ]
    
    def invoke(self, query: str) -> Dict:
        result = self.agent.invoke({"messages": [("user", query)]})
        return {"answer": result["messages"][-1].content}
