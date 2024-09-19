from sentient import sentient
import asyncio

custom_instructions = """
1. Directly go to youtube.com rather than searching for the song on google!
"""

# #use with open ai
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube", 
    task_instructions=custom_instructions,
    provider="openai",
    model="gpt-4o-2024-08-06"))

# #use with together ai
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube", 
    task_instructions=custom_instructions, 
    provider="together",
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"))

# #use with ollama
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube", 
    task_instructions=custom_instructions, 
    provider="ollama",
    model="llama3"))

#using anthropic
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube", 
    task_instructions=custom_instructions, 
    provider="anthropic",
    model="claude-3-5-sonnet-20240620"))

# use with groq models 
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube", 
    task_instructions=custom_instructions, 
    provider="groq",
    model="llama-3.1-70b-versatile"))

#using a custom endpoint (like remotely hosted vLLM/ ollama servers) 
#endpoint must be openai compatible
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube", 
    task_instructions=custom_instructions,
    provider="custom",
    custom_base_url="http://localhost:8080/v1",
    model="llama3.1"))

print(result)