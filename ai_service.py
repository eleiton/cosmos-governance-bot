import json
import typing_extensions
import google.generativeai as genai


class AiAssessment(typing_extensions.TypedDict):
    rating: int
    reason: str


class AIService:
    """Service class for handling AI-powered proposal assessments"""
    
    def __init__(self, api_key: str, model_name: str, instructions_file: str = "instructions.md"):
        """
        Initialize the AI service
        
        Args:
            api_key: Google Gemini API key
            model_name: Name of the Gemini model to use
            instructions_file: Path to the instructions markdown file
        """
        self.api_key = api_key
        self.model_name = model_name
        self.instructions_file = instructions_file
        self.instructions = self._load_instructions()
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def _load_instructions(self) -> str:
        """Load assessment instructions from file"""
        try:
            with open(self.instructions_file, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Instructions file '{self.instructions_file}' not found")
        except Exception as e:
            raise Exception(f"Error loading instructions: {e}")
    
    async def assess_proposal(self, summary: str) -> AiAssessment:
        """
        Assess a governance proposal using AI
        
        Args:
            summary: The proposal summary to assess
            
        Returns:
            AiAssessment containing rating and reason
            
        Raises:
            Exception: If AI assessment fails
        """
        try:
            prompt = f"{self.instructions}\n\n{summary}"
            
            response = self.model.generate_content(
                prompt, 
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json", 
                    response_schema=AiAssessment
                )
            )
            
            # Parse the JSON response
            assessment_data = json.loads(response.text)
            return AiAssessment(
                rating=assessment_data.get('rating', 0),
                reason=assessment_data.get('reason', 'No reason provided')
            )
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI response: {e}")
        except Exception as e:
            raise Exception(f"AI assessment failed: {e}")
    
    def format_assessment_message(self, assessment: AiAssessment) -> str:
        """
        Format the AI assessment into a visually appealing Telegram message
        
        Args:
            assessment: The AI assessment data
            
        Returns:
            Formatted message string
        """
        rating = assessment['rating']
        reason = assessment['reason']
        
        # Create rating emoji and text based on score
        if rating >= 8:
            rating_emoji = "🟢"
            rating_text = "STRONG SUPPORT"
        elif rating >= 6:
            rating_emoji = "🟡" 
            rating_text = "MODERATE SUPPORT"
        elif rating >= 4:
            rating_emoji = "🟠"
            rating_text = "NEUTRAL/CAUTION"
        else:
            rating_emoji = "🔴"
            rating_text = "NOT RECOMMENDED"
        
        return f"""🤖 **AI Assessment**

{rating_emoji} **{rating_text}** ({rating}/10)

**Analysis:**
{reason}

━━━━━━━━━━━━━━━━━━━━━
*This is an automated assessment for informational purposes only. Please conduct your own research before voting.*"""