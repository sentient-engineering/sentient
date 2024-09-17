# sentient - browser controlling agents in 3 lines of code

[beta]

```python
from sentient import sentient
import asyncio
result = asyncio.run(sentient.invoke(goal="play shape of you on youtube"))
```

### setup

1. install sentient `pip install sentient`

2. currently, you need to start chrome in dev mode - in a seaparate terminal on the port 9222. use the below commands to start the chrome instance and do necesssary logins if needed

for mac, use command -

```bash
sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

to run brave browser (mac) -

```bash
sudo /Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222 --guest
```

for linux -

```bash
google-chrome --remote-debugging-port=9222
```

for windows -

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

4. setup open ai api key in a .env file or `export OPENAI_API_KEY="sk-proj-"`

5. run the agent

```python
from sentient import sentient
import asyncio

# if you wanna run in a jupyter notebook, uncomment the following two lines :
#import nest_asyncio
#nest_asyncio.apply()

result = asyncio.run(sentient.invoke("play shape of you on youtube"))
```

6. note - by default we use `gpt-4o-2024-08-06` from `openai` to run sentient as it is the best performing model. you can also use other models like `gpt4o` or `gpt4o-mini` but the reliabilty may take some hit.

---

### setting custom task specific instructions

you can customise the agent's behaviour by providing natural language descripition of how it should naviagate or what all things it should keep in mind while executing a particualr task.
this is helpful in improving the accuracy and reliability of the agent on your specific task.

```
from sentient import sentient
import asyncio

custom_instructions = """
1. Directly go to youtube.com rather than searching for the song on google!
"""

#use with open ai
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube",
    task_instructions=custom_instructions,
    provider="openai",
    model="gpt-4o-2024-08-06"))
```

---

### using providers other than open ai

we currently support togehter ai and ollama as providers. if you wish to have others included, please create a new issue. you can pass custom instructions in a similar fashion as shown above. you can also refer the [cookbook](cookbook.py) for seeing all examples of using sentient with various providers.

#### using together ai hosted models

1. set API key for Together AI - `export TOGETHER_API_KEY="your-api-key"`

2. pass provider and model options to the invoke command.

```
#use with together ai
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube",
    provider="together",
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"))
```

#### using ollama

1. ensure the ollama server is on. you just need to pass the name of the model.

```
#use with ollama
result = asyncio.run(sentient.invoke(
    goal="play shape of you on youtube",
    provider="ollama",
    model="llama3"))
```
