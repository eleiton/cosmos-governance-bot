import requests
import json
import sys
import asyncio
from telegram.ext import ContextTypes
from ai_service import AIService
from telegram_service import TelegramService

CONFIG_FILE_PATH = "config.json"

def load_config():
    """Load configuration from JSON file, exit if file doesn't exist or is invalid"""
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{CONFIG_FILE_PATH}' not found.")
        print("Please create config.json with the required settings.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{CONFIG_FILE_PATH}': {e}")
        sys.exit(1)

    return config


def save_config(config):
    """Save configuration to JSON file"""
    with open(CONFIG_FILE_PATH, 'w') as f:
        json.dump(config, f, indent=2)


async def fetch_proposals():
    """Fetch proposals from the API"""
    try:
        response = requests.get(config["proposalsApi"], timeout=30)
        response.raise_for_status()
        data = response.json()
        proposals = data.get('proposals', [])
        # Reverse order to process proposals in ascending order (oldest first)
        return proposals[::-1]
    except requests.RequestException as e:
        print(f"Error fetching proposals: {e}")
        return []


async def send_new_proposal_notification(proposal):
    """Send notification for new proposals"""
    proposal_id = proposal['id']
    summary = proposal.get('summary', 'No summary available')

    # Load config to get chat details
    config = load_config()
    chat_id = int(config["governanceChannelId"])

    # Get AI assessment
    ai_assessment = None
    try:
        ai_assessment = await ai_service.assess_proposal(summary)
    except Exception as e:
        print(f"Error fetching ai assessment: {e}")

    try:
        # Use Telegram service to create topic and send messages
        thread_id = await telegram_service.create_proposal_topic(
            chat_id=chat_id,
            proposal=proposal,
            ai_service=ai_service,
            ai_assessment=ai_assessment
        )

        # Store thread ID in config
        config["proposalThreads"][str(proposal_id)] = thread_id
        save_config(config)
        
        # Sleep to avoid rate limiting
        await asyncio.sleep(10)
        
    except Exception as e:
        print(f"Error creating forum topic for proposal {proposal_id}: {e}")

async def check_proposals(context: ContextTypes.DEFAULT_TYPE = None):
    """Main task to check for new and ending proposals"""
    try:
        # Load current values
        config = load_config()
        if not config['ready']:
            return

        last_new_id = config["lastNewProposalId"]
        last_end_id = config["lastEndProposalId"]

        # Fetch proposals
        proposals = await fetch_proposals()
        if not proposals:
            return

        highest_new_id = last_new_id
        highest_end_id = last_end_id

        for proposal in proposals:
            proposal_id = int(proposal['id'])

            # Check for new proposals
            if proposal_id > last_new_id and proposal.get('status', '') in ['PROPOSAL_STATUS_VOTING_PERIOD']:
                await send_new_proposal_notification(proposal)
                highest_new_id = max(highest_new_id, proposal_id)

        # Update config with the highest IDs that were notified
        if highest_new_id > last_new_id or highest_end_id > last_end_id:
            # Reload config to get any thread mappings added during execution
            config = load_config()
            config["lastNewProposalId"] = max(highest_new_id, last_new_id)
            config["lastEndProposalId"] = max(highest_end_id, last_end_id)
            save_config(config)

    except Exception as e:
        print(f"Error in check_proposals: {e}")


if __name__ == "__main__":
    config = load_config()

    # Initialize services
    ai_service = AIService(
        api_key=config["aiToken"],
        model_name=config["aiModel"],
        instructions_file="instructions.md"
    )
    
    telegram_service = TelegramService(
        bot_token=config['telegramToken']
    )

    asyncio.run(check_proposals())
