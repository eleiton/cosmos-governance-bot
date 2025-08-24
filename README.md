# Cosmos Governance Bot

An intelligent Telegram bot that monitors Cosmos blockchain governance proposals and provides AI-powered security assessments to help protect the network from malicious proposals.

## 🤖 Live Bot Access

**🔗 Join the Osmosis bot: [https://t.me/osmosis_governance](https://t.me/osmosis_governance)**

The bot is currently running and actively monitoring Osmosis governance proposals. Join the channel to receive real-time notifications and AI security assessments for all new proposals.

**🌐 Expanding to More Chains**: Additional bots for other Cosmos chains (Cosmos Hub, Neutron, Injective, etc.) can be deployed on demand. Contact us if you'd like governance monitoring for your preferred chain.

## 🛡️ Security Benefits for Blockchain Governance

### Early Threat Detection
- **Automated Monitoring**: Continuously scans for new governance proposals every 30 minutes
- **Immediate Alerts**: Instantly notifies the community when new proposals are submitted
- **Proactive Defense**: Catches potentially harmful proposals before they gain momentum

### AI-Powered Security Analysis
- **Risk Assessment**: Uses AI to evaluate proposals for security vulnerabilities
- **Threat Classification**: Automatically rates proposals from 1-10 based on risk level
- **Visual Security Indicators**: 
  - 🔴 **NOT RECOMMENDED** (1-3/10) - High risk proposals
  - 🟠 **NEUTRAL/CAUTION** (4-5/10) - Requires careful review
  - 🟡 **MODERATE SUPPORT** (6-7/10) - Generally safe with minor concerns
  - 🟢 **STRONG SUPPORT** (8-10/10) - Low risk, beneficial proposals

### Comprehensive Security Evaluation

The AI analyzes proposals across multiple security dimensions:

#### **Technical Security**
- Smart contract vulnerabilities
- Protocol attack vectors
- Dependency risks
- Implementation safety mechanisms

#### **Economic Security**
- Tokenomics manipulation attempts
- Inflation/deflation attacks
- Staking reward exploitation
- Market manipulation risks

#### **Governance Security**
- Centralization attempts
- Voter manipulation tactics
- Threshold bypassing
- Democratic process integrity

#### **Operational Security**
- Network stability risks
- Validator impact assessment
- Downtime probability
- Recovery mechanisms

## 🔧 Technical Architecture

### Clean Service-Based Design
```
├── main.py              # Core orchestration
├── ai_service.py        # AI assessment engine
├── telegram_service.py  # Telegram bot operations
└── instructions.md      # AI evaluation criteria
```

### Key Components

#### **AIService**
- Gemini AI integration for proposal analysis
- Structured assessment with rating and reasoning
- Configurable evaluation criteria

#### **TelegramService** 
- Forum topic creation for each proposal
- Formatted message delivery
- Rate limiting protection

#### **Main Orchestrator**
- Proposal monitoring and processing
- Configuration management
- Service coordination

## 📋 Requirements

- Python 3.9+
- Telegram Bot Token
- Google Gemini AI API Key
- Telegram Channel with Forum Features

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cosmos-governance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create configuration file:
```json
{
  "telegramToken": "YOUR_TELEGRAM_BOT_TOKEN",
  "governanceChannelId": "YOUR_CHANNEL_ID",
  "aiToken": "YOUR_GEMINI_API_KEY",
  "aiModel": "YOUR_GEMINI_MODEL",
  "proposalsApi": "THE_COSMOS_GOVERNANCE_API",
  "lastNewProposalId": 0,
  "lastEndProposalId": 0
}
```

4. Run the bot:
```bash
python main.py
```

## 🛡️ Security Impact

### For Individual Users
- **Risk Awareness**: Understand potential threats before voting
- **Time Efficiency**: Get quick security summaries instead of manual analysis
- **Confidence**: Make informed decisions with AI-backed insights

### For the Network
- **Collective Intelligence**: Community benefits from automated threat detection
- **Faster Response**: Rapid identification of malicious proposals
- **Reduced Attack Surface**: Proactive security posture

### For Validators
- **Due Diligence**: Enhanced proposal review process
- **Reputation Protection**: Avoid supporting harmful proposals
- **Network Responsibility**: Contribute to ecosystem security

## 🔍 Example Security Assessment

```
🤖 AI Assessment

🟠 NEUTRAL/CAUTION (4/10)

Analysis:
This proposal modifies core staking parameters without sufficient 
testing documentation. While the economic rationale is sound, 
the implementation lacks security audits and rollback mechanisms. 
Recommend requiring additional safety measures before approval.

━━━━━━━━━━━━━━━━━━━━━
*This is an automated assessment for informational purposes 
only. Please conduct your own research before voting.*
```

## 🤝 Contributing

We welcome contributions that enhance the security and functionality of blockchain governance:

- **Security Improvements**: Enhanced threat detection algorithms
- **Analysis Criteria**: Additional security evaluation dimensions  
- **Integration**: Support for other Cosmos chains
- **Documentation**: Security best practices and guides

## ⚠️ Disclaimer

This bot provides automated analysis for educational and informational purposes only. Users should:

- Conduct independent research before voting
- Verify AI assessments through multiple sources
- Understand that no automated system is infallible
- Take responsibility for their voting decisions


---

**Protecting blockchain governance through intelligent automation and community empowerment.**