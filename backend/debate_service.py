from src.debate_engine.conversation_manager import start_debate

def process_debate(initial_question: str, mode: str = "standard", max_turns: int = 4):
    transcript = start_debate(initial_question, mode=mode, max_turns=max_turns)
    return transcript