# from groq import Groq
# from dotenv import load_dotenv
# import os


# load_dotenv()
# key = os.getenv("GROQ_API_KEY")
# print(key[:12] if key else None)
# client = Groq()

# response = client.chat.completions.create(
#     model="openai/gpt-oss-20b",
#     messages=[
#         {
#             "role": "user",
#             "content": "What is cancer?"
#         }
#     ]
# )

# print(response.choices[0].message.content)