from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from tavily import TavilyClient
from typing import Dict, Optional, List, Any
from pydantic import BaseModel, Field
import os
load_dotenv()


# Pydantic models for validation
class SearchResult(BaseModel):
    """Individual search result item"""
    url: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    score: Optional[float] = None
    raw_content: Optional[str] = None
    error: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow additional properties

class WebSearchOutput(BaseModel):
    """Output schema for web search results"""
    result: List[SearchResult] = Field(
        ..., 
        title="Result", 
        description="A list of search results"
    )

if "TAVILY_API_KEY" not in os.environ:
    raise ValueError("Missing TAVILY_API_KEY environment variable")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

mcp =  FastMCP(
    name="basic_web_search", 
    stateless_http=True
)

   


@mcp.tool()
def web_search(query: str) -> WebSearchOutput:
    """Use this tool to search the web for information
    using Tavily API.

    Args:
        query (str): The search query.

    Returns:
        WebSearchOutput: A validated object containing search results.
    """
    try:
        response = tavily_client.search(
            query=query,
            max_results=5
        )
        
        # Extract and validate results
        if isinstance(response, dict) and 'results' in response:
            search_results = [SearchResult(**result) for result in response['results']]
            return WebSearchOutput(result=search_results)
        else:
            # Return empty results
            return WebSearchOutput(result=[])
            
    except Exception as e:
        # Return error result
        error_result = SearchResult(error=f"Search failed for query '{query}': {str(e)}")
        return WebSearchOutput(result=[error_result])
    
    
