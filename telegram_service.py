from datetime import datetime, timezone
from telegram import Bot
from ai_service import AiAssessment, AIService


class TelegramService:
    """Service class for handling Telegram bot operations"""
    
    def __init__(self, bot_token: str):
        """
        Initialize the Telegram service
        
        Args:
            bot_token: Telegram bot token
        """
        self.bot = Bot(token=bot_token)
    
    def _parse_iso_datetime(self, iso_string: str) -> datetime:
        """Parse ISO datetime string to datetime object"""
        # Replace Z with timezone info
        dt_string = iso_string.replace('Z', '+00:00')

        # Handle microseconds with more than 6 digits (Python supports max 6)
        if '.' in dt_string and '+' in dt_string:
            # Split into datetime part and timezone part
            dt_part, tz_part = dt_string.rsplit('+', 1)
            if '.' in dt_part:
                # Split datetime into base and microseconds
                base_dt, microseconds_part = dt_part.split('.')
                # Truncate microseconds to 6 digits maximum
                microseconds_part = microseconds_part[:6].ljust(6, '0')
                # Reconstruct the datetime string
                dt_string = f"{base_dt}.{microseconds_part}+{tz_part}"

        return datetime.fromisoformat(dt_string)

    def _time_until_end(self, voting_end_time: str) -> float:
        """Calculate hours until voting end time"""
        end_time = self._parse_iso_datetime(voting_end_time)
        now = datetime.now(timezone.utc)
        time_diff = end_time - now
        return time_diff.total_seconds() / 3600  # Convert to hours

    def _format_proposal_message(self, proposal: dict) -> str:
        """
        Format a proposal into a visually appealing message
        
        Args:
            proposal: Proposal data from the API
            
        Returns:
            Formatted message string
        """
        proposal_id = proposal['id']
        title = proposal.get('title', 'Unknown Title')
        voting_start_time = proposal['voting_start_time']
        voting_end_time = proposal['voting_end_time']
        summary = proposal.get('summary', 'No summary available')

        # Truncate summary if too long
        if len(summary) > 1000:
            summary = summary[:1000] + "..."

        # Format dates to be more readable
        start_date = self._parse_iso_datetime(voting_start_time).strftime("%B %d, %Y at %H:%M UTC")
        end_date = self._parse_iso_datetime(voting_end_time).strftime("%B %d, %Y at %H:%M UTC")
        
        # Calculate voting period
        hours_remaining = self._time_until_end(voting_end_time)
        days_remaining = int(hours_remaining / 24)
        
        return f"""📋 **{title}**

{summary}

━━━━━━━━━━━━━━━━━━━━━
⏰ **Voting Period**
🗳️ Started: {start_date}
🔚 Ends: {end_date}
⏳ Time remaining: ~{days_remaining} days

🔗 [View on Mintscan](https://www.mintscan.io/osmosis/proposals/{proposal_id})

"""

    async def create_proposal_topic(self, chat_id: int, proposal: dict, ai_service: AIService = None, ai_assessment: AiAssessment = None) -> int:
        """
        Create a new forum topic for a proposal and send the proposal details
        
        Args:
            chat_id: Telegram chat ID where to create the topic
            proposal: Proposal data from the API
            ai_service: AIService instance for formatting assessment
            ai_assessment: Optional AI assessment to include
            
        Returns:
            The thread ID of the created topic
            
        Raises:
            Exception: If topic creation or message sending fails
        """
        proposal_id = proposal['id']
        
        try:
            # Create a new forum topic for the proposal
            topic = await self.bot.create_forum_topic(
                chat_id=chat_id,
                name=f"Proposal #{proposal_id}"
            )
            
            # Format and send the proposal details
            proposal_message = self._format_proposal_message(proposal)
            await self.bot.send_message(
                chat_id=chat_id,
                message_thread_id=topic.message_thread_id,
                text=proposal_message,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )

            # Send AI assessment as follow-up message if available
            if ai_assessment and ai_service:
                try:
                    assessment_message = ai_service.format_assessment_message(ai_assessment)
                    
                    await self.bot.send_message(
                        chat_id=chat_id,
                        message_thread_id=topic.message_thread_id,
                        text=assessment_message,
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
                    
                except Exception as e:
                    print(f"Error sending AI assessment: {e}")

            print(f'New proposal #{proposal_id} sent to forum topic {topic.message_thread_id}')
            return topic.message_thread_id
            
        except Exception as e:
            raise Exception(f"Error creating forum topic for proposal {proposal_id}: {e}")

    async def send_message(self, chat_id: int, text: str, thread_id: int = None) -> None:
        """
        Send a message to a chat or thread
        
        Args:
            chat_id: Telegram chat ID
            text: Message text
            thread_id: Optional thread ID for forum topics
        """
        await self.bot.send_message(
            chat_id=chat_id,
            message_thread_id=thread_id,
            text=text,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )