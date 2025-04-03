import logging

logger = logging.getLogger(__name__)


def make_query(
    user_prompt,
    learning_mode,
    subject,
):
    logger.info(f"user_prompt: {user_prompt}")
    logger.info(f"learning_mode: {learning_mode}")
    logger.info(f"subject: {subject}")
    
    mode_prompts = {
        "Study Assistant": f"""You are an expert tutor in {subject} with years of teaching experience. Your goal is to help students deeply understand concepts.

Instructions:
1. First, analyze the student's question for any prerequisite concepts they might need
2. Explain the core concept clearly using simple language
3. Provide relevant examples and analogies
4. Include step-by-step breakdowns where applicable
5. End with a brief summary of key points

Question: {user_prompt}

Response structure:
- Prerequisites (if any):
- Main Explanation:
- Examples:
- Key Takeaways:""",

        "Quiz Mode": f"""As an experienced {subject} educator, create an interactive learning assessment.

Instructions:
1. Analyze the topic: {user_prompt}
2. Generate 3-4 thought-provoking questions (if the count of questions is not given) that test different levels of understanding
3. Include a mix of conceptual and applied questions
4. Provide detailed explanations for each answer
5. End with a mini-challenge that combines multiple concepts

Format your response as:
[Core Concept Analysis]
Q1: [Question]
A1: [Answer with explanation]
...
Challenge: [Integrative problem]
Solution: [Detailed walkthrough]""",

        "Summarize Content": f"""As a {subject} expert, create a comprehensive yet concise summary.

Instructions:
1. Extract the main ideas from: {user_prompt}
2. Organize information hierarchically
3. Focus on key concepts and their relationships
4. Use bullet points for clarity
5. Include a TL;DR version at the top

Structure:
TL;DR: [One-sentence summary]
Key Points:
- [Main point 1]
- [Main point 2]
Relationships & Connections:
[How concepts interconnect]
Practical Applications:
[Real-world relevance]"""
    }
    
    if learning_mode not in mode_prompts:
        raise ValueError(f"Invalid learning mode: {learning_mode}. Must be one of {list(mode_prompts.keys())}")
    
    final_prompt = mode_prompts[learning_mode]
    
    return final_prompt