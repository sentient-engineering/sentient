# Sentient - Browser Controlling Agents in 3 Lines of Code

[Beta]

```python
from sentient import sentient
import asyncio
result = asyncio.run(sentient.invoke(goal="play shape of you on youtube"))
```

## Setup

1. Install sentient:
   ```
   pip install sentient
   ```

2. Start Chrome in dev mode on port 9222 in a separate terminal. Use the appropriate command for your operating system:

   MacOS (Chrome):
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --guest
   ```

   MacOS (Chromium):
   ```bash
   /Applications/Chromium.app/Contents/MacOS/Chromium --remote-debugging-port=9222 --guest
   ```

   MacOS (Brave):
   ```bash
   sudo /Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222 --guest
   ```

   Linux:
   ```bash
   google-chrome --remote-debugging-port=9222
   ```

   Windows:
   ```bash
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
   ```

3. Set up OpenAI API key:
   Create a `.env` file or use:
   ```
   export OPENAI_API_KEY="sk-proj-"
   ```

4. Run the agent:
   ```python
   from sentient import sentient
   import asyncio

   # If you want to run in a Jupyter notebook, uncomment the following two lines:
   # import nest_asyncio
   # nest_asyncio.apply()

   result = asyncio.run(sentient.invoke("play shape of you on youtube"))
   ```

   Note: If running in a Jupyter notebook, you need to uncomment and use the `nest_asyncio` lines as shown above.

5. Note: By default, we use `gpt-4-0824` from `openai` to run sentient as it is the best performing model. You can also use other models like `gpt4` or `gpt4-32k`, but reliability may be affected.

## Setting Custom Task-Specific Instructions

You can customize the agent's behavior by providing natural language instructions:

```python
from sentient import sentient
import asyncio

custom_instructions = """
1. Directly go to youtube.com rather than searching for the song on Google!
"""

# Use with OpenAI
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube",
    task_instructions=custom_instructions,
    provider="openai",
    model="gpt-4-0824"))
```

## Using Providers Other Than OpenAI

We currently support Together AI and Ollama as providers. If you wish to have others included, please create a new issue.

For more examples of using Sentient with various providers, refer to the [cookbook](cookbook.py).

### Using Together AI Hosted Models

1. Set API key for Together AI:
   ```
   export TOGETHER_API_KEY="your-api-key"
   ```

2. Pass provider and model options to the invoke command:
   ```python
   result = asyncio.run(sentient.invoke(
       goal="play shape of you on youtube",
       provider="together",
       model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"))
   ```

### Using Ollama

Ensure the Ollama server is on. You just need to pass the name of the model:

```python
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube",
    provider="ollama",
    model="llama3"))
```
