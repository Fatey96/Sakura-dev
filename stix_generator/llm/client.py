"""
LLM client wrapper.
"""

import os
import json
from typing import Dict, Any, List, Optional, Union

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel

from ..config import (
    OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE
)
from ..utils.logging_utils import setup_logger

logger = setup_logger("stix_generator.llm.client")

class LLMClient:
    """LLM client wrapper class."""
    
    def __init__(
        self, 
        api_key: str = OPENAI_API_KEY, 
        model: str = LLM_MODEL, 
        temperature: float = LLM_TEMPERATURE
    ):
        """
        Initialize the LLM client.
        
        Args:
            api_key: OpenAI API key
            model: LLM model to use
            temperature: Generation temperature
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        
        if not api_key:
            logger.warning("No API key provided. LLM client will not be functional.")
            self.llm = None
            return
            
        try:
            self.llm = ChatOpenAI(
                model=model,
                temperature=temperature,
                openai_api_key=api_key
            )
        except Exception as e:
            logger.error(f"Error initializing LLM client: {str(e)}")
            self.llm = None
    
    def create_chain(self, prompt_template: str, output_parser: Optional[JsonOutputParser] = None):
        """
        Create a LangChain chain with the given prompt template and output parser.
        
        Args:
            prompt_template: The prompt template string
            output_parser: Optional JsonOutputParser to parse the output
            
        Returns:
            A LangChain chain
        """
        if not self.llm:
            logger.error("LLM client not initialized properly")
            return None
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        if output_parser:
            chain = prompt | self.llm | output_parser
        else:
            chain = prompt | self.llm
            
        return chain
    
    async def ainvoke_chain(self, chain, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a LangChain chain asynchronously.
        
        Args:
            chain: The LangChain chain to invoke
            inputs: The inputs to the chain
            
        Returns:
            The output of the chain
        """
        if not chain:
            logger.error("Chain not initialized properly")
            return {}
            
        try:
            result = await chain.ainvoke(inputs)
            return result
        except Exception as e:
            logger.error(f"Error invoking chain: {str(e)}")
            return {}

def get_llm_client(
    api_key: str = OPENAI_API_KEY, 
    model: str = LLM_MODEL, 
    temperature: float = LLM_TEMPERATURE
) -> LLMClient:
    """
    Get an LLM client instance.
    
    Args:
        api_key: OpenAI API key
        model: LLM model to use
        temperature: Generation temperature
        
    Returns:
        LLM client instance
    """
    return LLMClient(
        api_key=api_key,
        model=model,
        temperature=temperature
    )