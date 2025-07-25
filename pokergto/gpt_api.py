import requests
import os

api_key = os.getenv("OPENAI_API_KEY")

def send_to_openai_parse_table(image_b64):
    prompt = """
Extract all visible information from the Texas Hold'em poker screenshot in a short and concise format. Include only:
- Hole cards
- Board cards
- Pot size (BB)
- Stack sizes (your stack and opponents)
- Blind level
- Current options (e.g. Fold, Check, Bet)
- Whether it's your turn
Output as a compact text list with no explanations.
"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
            ]
        }],
        "max_tokens": 500,
        "temperature": 0
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else None

def send_to_openai_gto_decision(parsed_text):
    gto_prompt = f"""
You are a professional poker analyst. I’m playing Zoom NL10 on GGPoker, where the rake is 8bb/100. Use an exploitative approach to help me maximize my EV and bb/100. Consider the following important characteristics of the player pool:

🔹 Pool Overview:
- 95% of players are regulars of various skill levels
- Most players are tight, risk-averse, and rarely bluff — especially on the river
- They fold frequently to c-bets in 3-bet pots
- They fold too often to check-raises, especially OOP
- They 3-bet often but 4-bet very rarely and only with a narrow range

🔹 Strategy Guidelines:
- Use a tight-aggressive (TAG) approach
- 3-bet and 4-bet aggressively vs CO and BTN opens, especially in position
- Prefer polarized 3-bet ranges
- Play fewer marginal spots out of position to avoid rake traps
- Use small c-bets (33%) on dry boards to exploit overfolding
- Delay c-bets or check-back medium-strength hands for pot control

🔹 Player Color Tags:
- Green = fishy tendencies (wide calls, limp, shortstacking, donk-bet, stack off light)
- Purple or no tag = average reg
- Short stack (<100bb) = assumed fish unless proven otherwise

🔹 EV Boosting Principles (to increase winrate):
- Exploit river passivity: overfold when facing aggression, overvalue when opponents check
- Fold A-high and K-high to river bets unless you block significant bluffs
- Don't bluff rivers frequently — pool calls too wide vs missed draws
- Bluff catch selectively with hands that block value
- Track who folds to 3-bets, check-raises, and turn barrels — and attack them
- Use high-frequency c-bet only vs unknowns or clear fish; play more balanced vs solid regs
- Game select by noticing stack sizes, timing, bet sizing tells

Here’s the hand:

{parsed_text}

Format your response exactly like this (single line):
EV(Fold): x.xx | EV(Check): x.xx | EV(Call): x.xx | EV(Bet Y BB): x.xx | EV(Raise): x.xx → ACTION
(Include only the actions that apply)
"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": gto_prompt}],
        "max_tokens": 200,
        "temperature": 0
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else None
