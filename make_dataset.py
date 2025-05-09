import os
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_DIR = os.path.join(BASE_DIR, "prompts")
MODEL = "gpt-4o"
TEMPERATURE = 0.7
GENERATE_QUESTION_NUMBER = 5

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=TEMPERATURE
    )
    return response.choices[0].message.content.strip()


def read_prompt(filename):
    with open(os.path.join(PROMPT_DIR, filename), "r", encoding="utf-8") as f:
        return f.read().strip()

def generate_item():
    # Load prompts
    sys_q = read_prompt("generate_question.txt")
    generate_one = read_prompt("generate_one.txt")
    user_q = read_prompt("generate_question_student.txt")
    sys_c = read_prompt("generate_chosen.txt")
    sys_r = read_prompt("generate_rejected.txt")

    # Generate prompt and responses
    question = ask_gpt(sys_q, generate_one) #문제 생성
    question_student = ask_gpt(question, user_q) #학생의 질문 생성
    chosen = ask_gpt(sys_c, question_student) #질문에 대한 잘못된 답변 생성
    rejected = ask_gpt(sys_r, question_student) #질문에 대한 올바른 답변 생성

    return {
        "question": question,
        "question_student" : question_student,
        "chosen": chosen,
        "rejected": rejected
    }

def generate_dataset(n=GENERATE_QUESTION_NUMBER, output_file="dpo_dataset.json"):
    data = []
    for i in range(n):
        print(f"Generating item {i+1}/{n}")
        data.append(generate_item())

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"저장 완료: {output_file} ({n}개 항목)")

if __name__ == "__main__":
    generate_dataset()
