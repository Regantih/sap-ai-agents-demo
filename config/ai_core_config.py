"""SAP AI Core Configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

class AICorConfig:
    """Configuration for SAP AI Core connection"""
    
    AI_CORE_CLIENT_ID = os.getenv("AICORE_CLIENT_ID")
    AI_CORE_CLIENT_SECRET = os.getenv("AICORE_CLIENT_SECRET")
    AI_CORE_AUTH_URL = os.getenv("AICORE_AUTH_URL")
    AI_CORE_API_URL = os.getenv("AICORE_BASE_URL")
    AI_CORE_RESOURCE_GROUP = os.getenv("AICORE_RESOURCE_GROUP", "default")
    LLM_DEPLOYMENT_ID = os.getenv("LLM_DEPLOYMENT_ID")
    EMBEDDING_DEPLOYMENT_ID = os.getenv("EMBEDDING_DEPLOYMENT_ID")
    ORCHESTRATION_DEPLOYMENT_URL = os.getenv("ORCHESTRATION_DEPLOYMENT_URL")

def set_environment_variables():
    """Set environment variables for SAP Gen AI Hub SDK"""
    os.environ["AICORE_AUTH_URL"] = AICorConfig.AI_CORE_AUTH_URL or ""
    os.environ["AICORE_CLIENT_ID"] = AICorConfig.AI_CORE_CLIENT_ID or ""
    os.environ["AICORE_CLIENT_SECRET"] = AICorConfig.AI_CORE_CLIENT_SECRET or ""
    os.environ["AICORE_BASE_URL"] = AICorConfig.AI_CORE_API_URL or ""
    os.environ["AICORE_RESOURCE_GROUP"] = AICorConfig.AI_CORE_RESOURCE_GROUP
