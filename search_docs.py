
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import http.client
import httpx
import json
import asyncio
from docling.document_converter import DocumentConverter


load_dotenv()

mcp = FastMCP("documents_from_web", stateless_http=True)

USER_AGENT = "docs-app/1.0.0"
SERPER_URL = "https://google.serper.dev/search"



docs_urls = {
   "langchain":"https://python.langchain.com/docs/",
   "llama_index":"https://docs.llamaindex.ai/en/stable/",
   "mcp":"https://mcp.readthedocs.io/en/latest/",
   "openai":"https://platform.openai.com/docs/",
}



async def search_web(query: str) -> dict | None:
    payload = {
        "q": query,
        "hl": "pt-br",
        "num": 2,
    }
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERPER_URL,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.reason_phrase}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
        
    

async def fetch_url(url: str) -> str:
    """
    Converte uma URL em markdown de forma assíncrona.
    Executa a conversão em uma thread separada para não bloquear o event loop.
    """
    def _convert_sync():
        converter = DocumentConverter()
        result = converter.convert(url)
        return result.document.export_to_markdown()
    
    # Executa a conversão síncrona em uma thread separada
    markdown_content = await asyncio.to_thread(_convert_sync)
    return markdown_content

@mcp.tool()
async def get_docs_from_web(query: str, library: str)-> list[dict] | str:
    """
    Search the docs for a given query and library.
    Supports libraries: langchain, llama_index, mcp, openai.

    Args:
        query (str): The query to search for (e.g., "how to use chains", "how to use agents").
        library (str): The library to search (e.g., "langchain")

    Returns:
        list[dict]: A list of documents found in the search.
    """
    
    if library not in docs_urls:
        raise ValueError(f"Library '{library}' not supported by this tool. Supported libraries: {', '.join(docs_urls.keys())}")
    
    query = f"site: {docs_urls[library]} {query}"
    results = await search_web(query)
    
    if not results or "organic" not in results or len(results["organic"]) == 0:
        return f"No results found for query: {query}"
    
    docs_list = []
    for result in results["organic"]:
        url = result.get("link")
        title = result.get("title", "Sem título")
        
        if url:
            try:
                content = await fetch_url(url)
                if content:
                    docs_list.append({
                        "source": url,
                        "content": content,
                        "title": title
                    })
            except Exception as e:
                print(f"Erro ao processar URL {url}: {e}")
    
    if not docs_list:
        return f"No content could be extracted for query: {query}"
    
    return docs_list
            
    

