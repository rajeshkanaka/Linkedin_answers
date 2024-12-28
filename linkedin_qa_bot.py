#!/usr/bin/env python3
"""
LinkedIn Q&A Bot using Claude 3.5 Sonnet
This script processes AI/ML questions and generates expert-level responses using Claude 3.5 Sonnet.
"""

import os
import re
import sys
import logging
import argparse
from dataclasses import dataclass
from typing import Optional, Tuple
import anthropic
from anthropic import Anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Question:
    """Data class to store question and description."""
    question: str
    description: str

class InputParser:
    """Handles parsing and validation of input text."""
    
    @staticmethod
    def parse_input(input_text: str) -> Optional[Question]:
        """
        Parse input text to extract question and description.
        
        Args:
            input_text: Raw input text containing XML-like tags
            
        Returns:
            Question object if parsing successful, None otherwise
        """
        try:
            question_match = re.search(r'<question>(.*?)<description>(.*?)</description>\s*</question>',
                                     input_text, re.DOTALL)
            if not question_match:
                logger.error("Invalid input format")
                return None
                
            question = question_match.group(1).strip()
            description = question_match.group(2).strip()
            return Question(question=question, description=description)
            
        except Exception as e:
            logger.error(f"Error parsing input: {str(e)}")
            return None

    @staticmethod
    def read_input_file(file_path: str) -> Optional[str]:
        """
        Read input from file.
        
        Args:
            file_path: Path to input file
            
        Returns:
            File contents if successful, None otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading input file: {str(e)}")
            return None

class PromptManager:
    """Manages prompt generation and formatting."""
    
    MASTER_PROMPT_TEMPLATE = """You are a senior expert-level AI/ML Developer answering questions for a LinkedIn audience of other AI professionals. You will be presented with a question related to AI and machine learning. Your task is to provide a well-structured, research-based answer that demonstrates your expertise while remaining accessible to your peers.

Here is the question you need to address:
<question>
{question}
</question>

Additional context:
{description}

When formulating your answer, follow these guidelines:
1. Use simple, clear English to explain complex concepts.
2. Provide easy-to-understand examples that are relevant to AI/ML developers.
3. Ensure your answer is mature, well-researched, and structured coherently.
4. Focus on delivering value to a LinkedIn audience of AI experts.
5. Keep your answer concise and to the point.

Very important: Your answer must not exceed 650 characters.

Provide your final answer within <answer> tags."""

    @classmethod
    def generate_prompt(cls, question: Question) -> str:
        """
        Generate formatted prompt for Claude.
        
        Args:
            question: Question object containing question and description
            
        Returns:
            Formatted prompt string
        """
        return cls.MASTER_PROMPT_TEMPLATE.format(
            question=question.question,
            description=question.description
        )

class ClaudeClient:
    """Handles interactions with Claude API."""
    
    def __init__(self):
        """Initialize Claude client with API key."""
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=self.api_key)

    def get_response(self, prompt: str) -> Optional[str]:
        """
        Get response from Claude API.
        
        Args:
            prompt: Formatted prompt string
            
        Returns:
            Claude's response if successful, None otherwise
        """
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            answer = response.content[0].text
            # Extract content between <answer> tags
            answer_match = re.search(r'<answer>(.*?)</answer>', answer, re.DOTALL)
            if answer_match:
                return answer_match.group(1).strip()
            return answer.strip()

        except Exception as e:
            logger.error(f"Error getting Claude response: {str(e)}")
            return None

class LinkedInQABot:
    """Main class orchestrating the Q&A process."""
    
    def __init__(self):
        """Initialize bot components."""
        self.input_parser = InputParser()
        self.prompt_manager = PromptManager()
        self.claude_client = ClaudeClient()

    def process_input(self, input_text: str) -> Optional[str]:
        """
        Process input and return Claude's response.
        
        Args:
            input_text: Raw input text
            
        Returns:
            Formatted response if successful, None otherwise
        """
        question_obj = self.input_parser.parse_input(input_text)
        if not question_obj:
            return None

        prompt = self.prompt_manager.generate_prompt(question_obj)
        response = self.claude_client.get_response(prompt)
        
        if response and len(response) > 650:
            logger.warning("Response exceeds 650 characters, truncating...")
            response = response[:647] + "..."
            
        return response

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate LinkedIn AI/ML expert responses using Claude 3.5 Sonnet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  %(prog)s                     # Use default input file (question&answerformat.md)
  %(prog)s -i custom_file.md   # Use custom input file
  %(prog)s --interactive       # Use interactive mode for input
        """
    )
    parser.add_argument('-i', '--input', 
                       default='question&answerformat.md',
                       help='Input file path (default: question&answerformat.md)')
    parser.add_argument('--interactive', 
                       action='store_true',
                       help='Use interactive mode for input')
    return parser.parse_args()

def interactive_input() -> str:
    """Get input interactively from user."""
    print("Enter your question and description (Ctrl+D or Ctrl+Z to submit):")
    input_lines = []
    while True:
        try:
            line = input()
            input_lines.append(line)
        except EOFError:
            break
    return "\n".join(input_lines)

def main():
    """Main function to run the bot."""
    args = parse_arguments()
    
    try:
        bot = LinkedInQABot()
        
        if args.interactive:
            input_text = interactive_input()
        else:
            input_text = InputParser.read_input_file(args.input)
            if not input_text:
                sys.exit(1)
        
        response = bot.process_input(input_text)
        
        if response:
            print("\nClaude's Response:")
            print("-" * 50)
            print(response)
            print("-" * 50)
        else:
            print("Failed to generate response. Please check the logs for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 