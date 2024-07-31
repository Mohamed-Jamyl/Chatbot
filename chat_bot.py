import json
from difflib import get_close_matches
from typing import List, Optional, Dict, Union

def load_base(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        data: Dict = json.load(file)
    return data

def save_base(file_path: str, data: Dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    matches: List = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, base: Dict) -> Optional[str]:
    for q in base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
    base: Dict = load_base('base.json')

    while True:
        user_input: str = input('You: ')
        if user_input.lower() == 'quit':
            break
        best_match: Optional[str] = find_best_match(user_input, [q['question'] for q in base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, base)
            print(f'Astrobot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                base['questions'].append({'question': user_input, 'answer': new_answer})
                save_base('base.json', base)
                print('Astrobot: Thanks, I learned a new response.')

if __name__ == '__main__':
    chat_bot()