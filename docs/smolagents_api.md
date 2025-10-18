Base Model
The Model class serves as the foundation for all model implementations, providing the core interface that custom models must implement to work with agents.
class smolagents.Model
<source>
( flatten_messages_as_text: bool = Falsetool_name_key: str = 'name'tool_arguments_key: str = 'arguments'model_id: str | None = None**kwargs )
Parameters
flatten_messages_as_text (bool, default False) — Whether to flatten complex message content into plain text format.
tool_name_key (str, default "name") — The key used to extract tool names from model responses.
tool_arguments_key (str, default "arguments") — The key used to extract tool arguments from model responses.
model_id (str, optional) — Identifier for the specific model being used.
**kwargs — Additional keyword arguments to forward to the underlying model completion call.
Base class for all language model implementations.
This abstract class defines the core interface that all model implementations must follow to work with agents. It provides common functionality for message handling, tool integration, and model configuration while allowing subclasses to implement their specific generation logic.
Note: This is an abstract base class. Subclasses must implement the generate() method to provide actual model inference capabilities.

Example:
Copied
class CustomModel(Model):
    def generate(self, messages, **kwargs):
        # Implementation specific to your model
        pass
generate
<source>
( messages: liststop_sequences: list[str] | None = Noneresponse_format: dict[str, str] | None = Nonetools_to_call_from: list[smolagents.tools.Tool] | None = None**kwargs ) → ChatMessage
Parameters
messages (list[dict[str, str | list[dict]]] | list[ChatMessage]) — A list of message dictionaries to be processed. Each dictionary should have the structure {"role": "user/system", "content": "message content"}.
stop_sequences (List[str], optional) — A list of strings that will stop the generation if encountered in the model’s output.
response_format (dict[str, str], optional) — The response format to use in the model’s response.
tools_to_call_from (List[Tool], optional) — A list of tools that the model can use to generate responses.
**kwargs — Additional keyword arguments to be passed to the underlying model.
Returns
ChatMessage

A chat message object containing the model’s response.

Process the input messages and return the model’s response.
parse_tool_calls
<source>
( message: ChatMessage )
Sometimes APIs do not return the tool call as a specific object, so we need to parse it.
to_dict
<source>
( )
Converts the model into a JSON-compatible dictionary.
API Model
The ApiModel class serves as the foundation for all API-based model implementations, providing common functionality for external API interactions, rate limiting, and client management that API-specific models inherit.
class smolagents.ApiModel
<source>
( model_id: strcustom_role_conversions: dict[str, str] | None = Noneclient: typing.Optional[typing.Any] = Nonerequests_per_minute: float | None = None**kwargs )
Parameters
model_id (str) — The identifier for the model to be used with the API.
custom_role_conversions (dict[str, str], optional) — Mapping to convert between internal role names and API-specific role names. Defaults to None.
client (Any, optional) — Pre-configured API client instance. If not provided, a default client will be created. Defaults to None.
requests_per_minute (float, optional) — Rate limit in requests per minute.
**kwargs — Additional keyword arguments to forward to the underlying model completion call.
Base class for API-based language models.
This class serves as a foundation for implementing models that interact with external APIs. It handles the common functionality for managing model IDs, custom role mappings, and API client connections.
create_client
<source>
( )
Create the API client for the specific service.
TransformersModel
For convenience, we have added a TransformersModel that implements the points above by building a local transformers pipeline for the model_id given at initialization.
Copied
from smolagents import TransformersModel

model = TransformersModel(model_id="HuggingFaceTB/SmolLM-135M-Instruct")

print(model([{"role": "user", "content": [{"type": "text", "text": "Ok!"}]}], stop_sequences=["great"]))
Copied
>>> What a
You can pass any keyword arguments supported by the underlying model (such as temperature, max_new_tokens, top_p, etc.) directly at instantiation time. These are forwarded to the model completion call:
Copied
model = TransformersModel(
    model_id="HuggingFaceTB/SmolLM-135M-Instruct",
    temperature=0.7,
    max_new_tokens=1000
)
You must have transformers and torch installed on your machine. Please run pip install 'smolagents[transformers]' if it’s not the case.
class smolagents.TransformersModel
<source>
( model_id: str | None = Nonedevice_map: str | None = Nonetorch_dtype: str | None = Nonetrust_remote_code: bool = Falsemodel_kwargs: dict[str, typing.Any] | None = Nonemax_new_tokens: int = 4096max_tokens: int | None = None**kwargs )
Expand 8 parameters
Parameters
model_id (str) — The Hugging Face model ID to be used for inference. This can be a path or model identifier from the Hugging Face model hub. For example, "Qwen/Qwen2.5-Coder-32B-Instruct".
device_map (str, optional) — The device_map to initialize your model with.
torch_dtype (str, optional) — The torch_dtype to initialize your model with.
trust_remote_code (bool, default False) — Some models on the Hub require running remote code: for this model, you would have to set this flag to True.
model_kwargs (dict[str, Any], optional) — Additional keyword arguments to pass to AutoModel.from_pretrained (like revision, model_args, config, etc.).
max_new_tokens (int, default 4096) — Maximum number of new tokens to generate, ignoring the number of tokens in the prompt.
max_tokens (int, optional) — Alias for max_new_tokens. If provided, this value takes precedence.
**kwargs — Additional keyword arguments to forward to the underlying Transformers model generate call, such as device.
Raises
ValueError

ValueError — If the model name is not provided.

A class that uses Hugging Face’s Transformers library for language model interaction.
This model allows you to load and use Hugging Face’s models locally using the Transformers library. It supports features like stop sequences and grammar customization.
You must have transformers and torch installed on your machine. Please run pip install 'smolagents[transformers]' if it’s not the case.

Example:
Copied
engine = TransformersModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    device="cuda",
    max_new_tokens=5000,
)
messages = [{"role": "user", "content": "Explain quantum mechanics in simple terms."}]
response = engine(messages, stop_sequences=["END"])
print(response)
"Quantum mechanics is the branch of physics that studies..."
InferenceClientModel
The InferenceClientModel wraps huggingface_hub’s InferenceClient for the execution of the LLM. It supports all Inference Providers available on the Hub: Cerebras, Cohere, Fal, Fireworks, HF-Inference, Hyperbolic, Nebius, Novita, Replicate, SambaNova, Together, and more.
You can also set a rate limit in requests per minute by using the requests_per_minute argument:
Copied
from smolagents import InferenceClientModel

messages = [
  {"role": "user", "content": [{"type": "text", "text": "Hello, how are you?"}]}
]

model = InferenceClientModel(provider="novita", requests_per_minute=60)
print(model(messages))
Copied
>>> Of course! If you change your mind, feel free to reach out. Take care!
You can pass any keyword arguments supported by the underlying model (such as temperature, max_tokens, top_p, etc.) directly at instantiation time. These are forwarded to the model completion call:
Copied
model = InferenceClientModel(
    provider="novita",
    requests_per_minute=60,
    temperature=0.8,
    max_tokens=500
)
class smolagents.InferenceClientModel
<source>
( model_id: str = 'Qwen/Qwen2.5-Coder-32B-Instruct'provider: str | None = Nonetoken: str | None = Nonetimeout: int = 120client_kwargs: dict[str, typing.Any] | None = Nonecustom_role_conversions: dict[str, str] | None = Noneapi_key: str | None = Nonebill_to: str | None = Nonebase_url: str | None = None**kwargs )
Expand 10 parameters
Parameters
model_id (str, optional, default "Qwen/Qwen2.5-Coder-32B-Instruct") — The Hugging Face model ID to be used for inference. This can be a model identifier from the Hugging Face model hub or a URL to a deployed Inference Endpoint. Currently, it defaults to "Qwen/Qwen2.5-Coder-32B-Instruct", but this may change in the future.
provider (str, optional) — Name of the provider to use for inference. A list of supported providers can be found in the Inference Providers documentation. Defaults to “auto” i.e. the first of the providers available for the model, sorted by the user’s order here. If base_url is passed, then provider is not used.
token (str, optional) — Token used by the Hugging Face API for authentication. This token need to be authorized ‘Make calls to the serverless Inference Providers’. If the model is gated (like Llama-3 models), the token also needs ‘Read access to contents of all public gated repos you can access’. If not provided, the class will try to use environment variable ‘HF_TOKEN’, else use the token stored in the Hugging Face CLI configuration.
timeout (int, optional, defaults to 120) — Timeout for the API request, in seconds.
client_kwargs (dict[str, Any], optional) — Additional keyword arguments to pass to the Hugging Face InferenceClient.
custom_role_conversions (dict[str, str], optional) — Custom role conversion mapping to convert message roles in others. Useful for specific models that do not support specific message roles like “system”.
api_key (str, optional) — Token to use for authentication. This is a duplicated argument from token to make InferenceClientModel follow the same pattern as openai.OpenAI client. Cannot be used if token is set. Defaults to None.
bill_to (str, optional) — The billing account to use for the requests. By default the requests are billed on the user’s account. Requests can only be billed to an organization the user is a member of, and which has subscribed to Enterprise Hub.
base_url (str, optional) — Base URL to run inference. This is a duplicated argument from model to make InferenceClientModel follow the same pattern as openai.OpenAI client. Cannot be used if model is set. Defaults to None.
**kwargs — Additional keyword arguments to forward to the underlying Hugging Face InferenceClient completion call.
Raises
ValueError

ValueError — If the model name is not provided.

A class to interact with Hugging Face’s Inference Providers for language model interaction.
This model allows you to communicate with Hugging Face’s models using Inference Providers. It can be used in both serverless mode, with a dedicated endpoint, or even with a local URL, supporting features like stop sequences and grammar customization.
Providers include Cerebras, Cohere, Fal, Fireworks, HF-Inference, Hyperbolic, Nebius, Novita, Replicate, SambaNova, Together, and more.

Example:
Copied
engine = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    provider="nebius",
    token="your_hf_token_here",
    max_tokens=5000,
)
messages = [{"role": "user", "content": "Explain quantum mechanics in simple terms."}]
response = engine(messages, stop_sequences=["END"])
print(response)
"Quantum mechanics is the branch of physics that studies..."
create_client
<source>
( )
Create the Hugging Face client.
LiteLLMModel
The LiteLLMModel leverages LiteLLM to support 100+ LLMs from various providers. You can pass kwargs upon model initialization that will then be used whenever using the model, for instance below we pass temperature. You can also set a rate limit in requests per minute by using the requests_per_minute argument.
Copied
from smolagents import LiteLLMModel

messages = [
  {"role": "user", "content": [{"type": "text", "text": "Hello, how are you?"}]}
]

model = LiteLLMModel(model_id="anthropic/claude-3-5-sonnet-latest", temperature=0.2, max_tokens=10, requests_per_minute=60)
print(model(messages))
class smolagents.LiteLLMModel
<source>
( model_id: str | None = Noneapi_base: str | None = Noneapi_key: str | None = Nonecustom_role_conversions: dict[str, str] | None = Noneflatten_messages_as_text: bool | None = None**kwargs )
Parameters
model_id (str) — The model identifier to use on the server (e.g. “gpt-3.5-turbo”).
api_base (str, optional) — The base URL of the provider API to call the model.
api_key (str, optional) — The API key to use for authentication.
custom_role_conversions (dict[str, str], optional) — Custom role conversion mapping to convert message roles in others. Useful for specific models that do not support specific message roles like “system”.
flatten_messages_as_text (bool, optional) — Whether to flatten messages as text. Defaults to True for models that start with “ollama”, “groq”, “cerebras”.
**kwargs — Additional keyword arguments to forward to the underlying LiteLLM completion call.
Model to use LiteLLM Python SDK to access hundreds of LLMs.
create_client
<source>
( )
Create the LiteLLM client.
LiteLLMRouterModel
The LiteLLMRouterModel is a wrapper around the LiteLLM Router that leverages advanced routing strategies: load-balancing across multiple deployments, prioritizing critical requests via queueing, and implementing basic reliability measures such as cooldowns, fallbacks, and exponential backoff retries.
Copied
from smolagents import LiteLLMRouterModel

messages = [
  {"role": "user", "content": [{"type": "text", "text": "Hello, how are you?"}]}
]

model = LiteLLMRouterModel(
    model_id="llama-3.3-70b",
    model_list=[
        {
            "model_name": "llama-3.3-70b",
            "litellm_params": {"model": "groq/llama-3.3-70b", "api_key": os.getenv("GROQ_API_KEY")},
        },
        {
            "model_name": "llama-3.3-70b",
            "litellm_params": {"model": "cerebras/llama-3.3-70b", "api_key": os.getenv("CEREBRAS_API_KEY")},
        },
    ],
    client_kwargs={
        "routing_strategy": "simple-shuffle",
    },
)
print(model(messages))
class smolagents.LiteLLMRouterModel
<source>
( model_id: strmodel_list: listclient_kwargs: dict[str, typing.Any] | None = Nonecustom_role_conversions: dict[str, str] | None = Noneflatten_messages_as_text: bool | None = None**kwargs )
Parameters
model_id (str) — Identifier for the model group to use from the model list (e.g., “model-group-1”).
model_list (list[dict[str, Any]]) — Model configurations to be used for routing. Each configuration should include the model group name and any necessary parameters. For more details, refer to the LiteLLM Routing documentation.
client_kwargs (dict[str, Any], optional) — Additional configuration parameters for the Router client. For more details, see the LiteLLM Routing Configurations.
custom_role_conversions (dict[str, str], optional) — Custom role conversion mapping to convert message roles in others. Useful for specific models that do not support specific message roles like “system”.
flatten_messages_as_text (bool, optional) — Whether to flatten messages as text. Defaults to True for models that start with “ollama”, “groq”, “cerebras”.
**kwargs — Additional keyword arguments to forward to the underlying LiteLLM Router completion call.
Router‑based client for interacting with the LiteLLM Python SDK Router.
This class provides a high-level interface for distributing requests among multiple language models using the LiteLLM SDK’s routing capabilities. It is responsible for initializing and configuring the router client, applying custom role conversions, and managing message formatting to ensure seamless integration with various LLMs.

Example:
Copied
import os
from smolagents import CodeAgent, WebSearchTool, LiteLLMRouterModel
os.environ["OPENAI_API_KEY"] = ""
os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
os.environ["AWS_REGION"] = ""
llm_loadbalancer_model_list = [
    {
        "model_name": "model-group-1",
        "litellm_params": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
    },
    {
        "model_name": "model-group-1",
        "litellm_params": {
            "model": "bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": os.getenv("AWS_REGION"),
        },
    },
]
model = LiteLLMRouterModel(
   model_id="model-group-1",
   model_list=llm_loadbalancer_model_list,
   client_kwargs={
       "routing_strategy":"simple-shuffle"
   }
)
agent = CodeAgent(tools=[WebSearchTool()], model=model)
agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts?")
OpenAIServerModel
This class lets you call any OpenAIServer compatible model. Here’s how you can set it (you can customise the api_base url to point to another server):
Copied
import os
from smolagents import OpenAIServerModel

model = OpenAIServerModel(
    model_id="gpt-4o",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)
You can pass any keyword arguments supported by the underlying model (such as temperature, max_tokens, top_p, etc.) directly at instantiation time. These are forwarded to the model completion call:
Copied
model = OpenAIServerModel(
    model_id="gpt-4o",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
    temperature=0.7,
    max_tokens=1000,
    top_p=0.9,
)
class smolagents.OpenAIServerModel
<source>
( model_id: strapi_base: str | None = Noneapi_key: str | None = Noneorganization: str | None = Noneproject: str | None = Noneclient_kwargs: dict[str, typing.Any] | None = Nonecustom_role_conversions: dict[str, str] | None = Noneflatten_messages_as_text: bool = False**kwargs )
Parameters
model_id (str) — The model identifier to use on the server (e.g. “gpt-3.5-turbo”).
api_base (str, optional) — The base URL of the OpenAI-compatible API server.
api_key (str, optional) — The API key to use for authentication.
organization (str, optional) — The organization to use for the API request.
project (str, optional) — The project to use for the API request.
client_kwargs (dict[str, Any], optional) — Additional keyword arguments to pass to the OpenAI client (like organization, project, max_retries etc.).
custom_role_conversions (dict[str, str], optional) — Custom role conversion mapping to convert message roles in others. Useful for specific models that do not support specific message roles like “system”.
flatten_messages_as_text (bool, default False) — Whether to flatten messages as text.
**kwargs — Additional keyword arguments to forward to the underlying OpenAI API completion call, for instance temperature.
This model connects to an OpenAI-compatible API server.
AzureOpenAIServerModel
AzureOpenAIServerModel allows you to connect to any Azure OpenAI deployment.
Below you can find an example of how to set it up, note that you can omit the azure_endpoint, api_key, and api_version arguments, provided you’ve set the corresponding environment variables — AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and OPENAI_API_VERSION.
Pay attention to the lack of an AZURE_ prefix for OPENAI_API_VERSION, this is due to the way the underlying openai package is designed.
Copied
import os

from smolagents import AzureOpenAIServerModel

model = AzureOpenAIServerModel(
    model_id = os.environ.get("AZURE_OPENAI_MODEL"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("OPENAI_API_VERSION")
)
class smolagents.AzureOpenAIServerModel
<source>
( model_id: strazure_endpoint: str | None = Noneapi_key: str | None = Noneapi_version: str | None = Noneclient_kwargs: dict[str, typing.Any] | None = Nonecustom_role_conversions: dict[str, str] | None = None**kwargs )
Parameters
model_id (str) — The model deployment name to use when connecting (e.g. “gpt-4o-mini”).
azure_endpoint (str, optional) — The Azure endpoint, including the resource, e.g. https://example-resource.azure.openai.com/. If not provided, it will be inferred from the AZURE_OPENAI_ENDPOINT environment variable.
api_key (str, optional) — The API key to use for authentication. If not provided, it will be inferred from the AZURE_OPENAI_API_KEY environment variable.
api_version (str, optional) — The API version to use. If not provided, it will be inferred from the OPENAI_API_VERSION environment variable.
client_kwargs (dict[str, Any], optional) — Additional keyword arguments to pass to the AzureOpenAI client (like organization, project, max_retries etc.).
custom_role_conversions (dict[str, str], optional) — Custom role conversion mapping to convert message roles in others. Useful for specific models that do not support specific message roles like “system”.
**kwargs — Additional keyword arguments to forward to the underlying Azure OpenAI API completion call.
This model connects to an Azure OpenAI deployment.
AmazonBedrockServerModel
AmazonBedrockServerModel helps you connect to Amazon Bedrock and run your agent with any available models.
Below is an example setup. This class also offers additional options for customization.
Copied
import os

from smolagents import AmazonBedrockServerModel

model = AmazonBedrockServerModel(
    model_id = os.environ.get("AMAZON_BEDROCK_MODEL_ID"),
)
class smolagents.AmazonBedrockServerModel
<source>
( model_id: strclient = Noneclient_kwargs: dict[str, typing.Any] | None = Nonecustom_role_conversions: dict[str, str] | None = None**kwargs )
Parameters
model_id (str) — The model identifier to use on Bedrock (e.g. “us.amazon.nova-pro-v1:0”).
client (boto3.client, optional) — A custom boto3 client for AWS interactions. If not provided, a default client will be created.
client_kwargs (dict[str, Any], optional) — Keyword arguments used to configure the boto3 client if it needs to be created internally. Examples include region_name, config, or endpoint_url.
custom_role_conversions (dict[str, str], optional) — Custom role conversion mapping to convert message roles in others. Useful for specific models that do not support specific message roles like “system”. Defaults to converting all roles to “user” role to enable using all the Bedrock models.
flatten_messages_as_text (bool, default False) — Whether to flatten messages as text.
**kwargs — Additional keyword arguments to forward to the underlying Amazon Bedrock model converse call.
A model class for interacting with Amazon Bedrock Server models through the Bedrock API.
This class provides an interface to interact with various Bedrock language models, allowing for customized model inference, guardrail configuration, message handling, and other parameters allowed by boto3 API.
Authentication:
Amazon Bedrock supports multiple authentication methods:
Default AWS credentials: Use the default AWS credential chain (e.g., IAM roles, IAM users).
API Key Authentication (requires boto3 >= 1.39.0): Set the API key using the AWS_BEARER_TOKEN_BEDROCK environment variable.
API key support requires boto3 >= 1.39.0. For users not relying on API key authentication, the minimum supported version is boto3 >= 1.36.18.
Examples:

Creating a model instance with default settings:
Copied
bedrock_model = AmazonBedrockServerModel(
    model_id='us.amazon.nova-pro-v1:0'
)

Creating a model instance with a custom boto3 client:
Copied
import boto3
client = boto3.client('bedrock-runtime', region_name='us-west-2')
bedrock_model = AmazonBedrockServerModel(
    model_id='us.amazon.nova-pro-v1:0',
    client=client
)

Creating a model instance with client_kwargs for internal client creation:
Copied
bedrock_model = AmazonBedrockServerModel(
    model_id='us.amazon.nova-pro-v1:0',
    client_kwargs={'region_name': 'us-west-2', 'endpoint_url': 'https://custom-endpoint.com'}
)

Creating a model instance with inference and guardrail configurations:
Copied
additional_api_config = {
    "inferenceConfig": {
        "maxTokens": 3000
    },
    "guardrailConfig": {
        "guardrailIdentifier": "identify1",
        "guardrailVersion": 'v1'
    },
}
bedrock_model = AmazonBedrockServerModel(
    model_id='anthropic.claude-3-haiku-20240307-v1:0',
    **additional_api_config
)
MLXModel
Copied
from smolagents import MLXModel

model = MLXModel(model_id="HuggingFaceTB/SmolLM-135M-Instruct")

print(model([{"role": "user", "content": "Ok!"}], stop_sequences=["great"]))
Copied
>>> What a
You must have mlx-lm installed on your machine. Please run pip install 'smolagents[mlx-lm]' if it’s not the case.
class smolagents.MLXModel
<source>
( model_id: strtrust_remote_code: bool = Falseload_kwargs: dict[str, typing.Any] | None = Noneapply_chat_template_kwargs: dict[str, typing.Any] | None = None**kwargs )
Parameters
model_id (str) — The Hugging Face model ID to be used for inference. This can be a path or model identifier from the Hugging Face model hub.
tool_name_key (str) — The key, which can usually be found in the model’s chat template, for retrieving a tool name.
tool_arguments_key (str) — The key, which can usually be found in the model’s chat template, for retrieving tool arguments.
trust_remote_code (bool, default False) — Some models on the Hub require running remote code: for this model, you would have to set this flag to True.
load_kwargs (dict[str, Any], optional) — Additional keyword arguments to pass to the mlx.lm.load method when loading the model and tokenizer.
apply_chat_template_kwargs (dict, optional) — Additional keyword arguments to pass to the apply_chat_template method of the tokenizer.
**kwargs — Additional keyword arguments to forward to the underlying MLX model stream_generate call, for instance max_tokens.
A class to interact with models loaded using MLX on Apple silicon.
You must have mlx-lm installed on your machine. Please run pip install 'smolagents[mlx-lm]' if it’s not the case.

Example:
Copied
engine = MLXModel(
    model_id="mlx-community/Qwen2.5-Coder-32B-Instruct-4bit",
    max_tokens=10000,
)
messages = [
    {
        "role": "user",
        "content": "Explain quantum mechanics in simple terms."
    }
]
response = engine(messages, stop_sequences=["END"])
print(response)
"Quantum mechanics is the branch of physics that studies..."
VLLMModel
Model to use vLLM for fast LLM inference and serving.
Copied
from smolagents import VLLMModel

model = VLLMModel(model_id="HuggingFaceTB/SmolLM-135M-Instruct")

print(model([{"role": "user", "content": "Ok!"}], stop_sequences=["great"]))
You must have vllm installed on your machine. Please run pip install 'smolagents[vllm]' if it’s not the case.
class smolagents.VLLMModel
<source>
( model_idmodel_kwargs: dict[str, typing.Any] | None = None**kwargs )
Parameters
model_id (str) — The Hugging Face model ID to be used for inference. This can be a path or model identifier from the Hugging Face model hub.
model_kwargs (dict[str, Any], optional) — Additional keyword arguments to forward to the vLLM LLM instantiation, such as revision, max_model_len, etc.
**kwargs — Additional keyword arguments to forward to the underlying vLLM model generate call.
Model to use vLLM for fast LLM inference and serving.
Custom Model
You’re free to create and use your own models to power your agent.
You could subclass the base Model class to create a model for your agent. The main criteria is to subclass the generate method, with these two criteria:
It follows the messages format (List[Dict[str, str]]) for its input messages, and it returns an object with a .content attribute.
It stops generating outputs at the sequences passed in the argument stop_sequences.
For defining your LLM, you can make a CustomModel class that inherits from the base Model class. It should have a generate method that takes a list of messages and returns an object with a .content attribute containing the text. The generate method also needs to accept a stop_sequences argument that indicates when to stop generating.
Copied
from huggingface_hub import login, InferenceClient

from smolagents import Model

login("<YOUR_HUGGINGFACEHUB_API_TOKEN>")

model_id = "meta-llama/Llama-3.3-70B-Instruct"

client = InferenceClient(model=model_id)

class CustomModel(Model):
    def generate(messages, stop_sequences=["Task"]):
        response = client.chat_completion(messages, stop=stop_sequences, max_tokens=1024)
        answer = response.choices[0].message
        return answer

custom_model = CustomModel()
Additionally, generate can also take a grammar argument to allow constrained generation in order to force properly-formatted agent outputs.Tools
Smolagents is an experimental API which is subject to change at any time. Results returned by the agents can vary as the APIs or underlying models are prone to change.
To learn more about agents and tools make sure to read the introductory guide. This page contains the API docs for the underlying classes.
Tool Base Classes
load_tool
smolagents.load_tool
<source>
( repo_idmodel_repo_id: str | None = Nonetoken: str | None = Nonetrust_remote_code: bool = False**kwargs )
Parameters
repo_id (str) — Space repo ID of a tool on the Hub.
model_repo_id (str, optional) — Use this argument to use a different model than the default one for the tool you selected.
token (str, optional) — The token to identify you on hf.co. If unset, will use the token generated when running huggingface-cli login (stored in ~/.huggingface).
trust_remote_code (bool, optional, defaults to False) — This needs to be accepted in order to load a tool from Hub.
kwargs (additional keyword arguments, optional) — Additional keyword arguments that will be split in two: all arguments relevant to the Hub (such as cache_dir, revision, subfolder) will be used when downloading the files for your tool, and the others will be passed along to its init.
Main function to quickly load a tool from the Hub.
Loading a tool means that you’ll download the tool and execute it locally. ALWAYS inspect the tool you’re downloading before loading it within your runtime, as you would do when installing a package using pip/npm/apt.
tool
smolagents.tool
<source>
( tool_function: Callable )
Parameters
tool_function (Callable) — Function to convert into a Tool subclass. Should have type hints for each input and a type hint for the output. Should also have a docstring including the description of the function and an ‘Args:’ part where each argument is described.
Convert a function into an instance of a dynamically created Tool subclass.
Tool
class smolagents.Tool
<source>
( *args**kwargs )
A base class for the functions used by the agent. Subclass this and implement the forward method as well as the following class attributes:
description (str) — A short description of what your tool does, the inputs it expects and the output(s) it will return. For instance ‘This is a tool that downloads a file from a url. It takes the url as input, and returns the text contained in the file’.
name (str) — A performative name that will be used for your tool in the prompt to the agent. For instance "text-classifier" or "image_generator".
inputs (Dict[str, Dict[str, Union[str, type, bool]]]) — The dict of modalities expected for the inputs. It has one typekey and a descriptionkey. This is used by launch_gradio_demo or to make a nice space from your tool, and also can be used in the generated description for your tool.
output_type (type) — The type of the tool output. This is used by launch_gradio_demo or to make a nice space from your tool, and also can be used in the generated description for your tool.
output_schema (Dict[str, Any], optional) — The JSON schema defining the expected structure of the tool output. This can be included in system prompts to help agents understand the expected output format. Note: This is currently used for informational purposes only and does not perform actual output validation.
You can also override the method setup() if your tool has an expensive operation to perform before being usable (such as loading a model). setup() will be called the first time you use your tool, but not at instantiation.
from_dict
<source>
( tool_dict: dict[str, Any]**kwargs ) → Tool
Parameters
tool_dict (dict[str, Any]) — Dictionary representation of the tool.
**kwargs — Additional keyword arguments to pass to the tool’s constructor.
Returns
Tool

Tool object.

Create tool from a dictionary representation.
from_gradio
<source>
( gradio_tool )
Creates a Tool from a gradio tool.
from_hub
<source>
( repo_id: strtoken: str | None = Nonetrust_remote_code: bool = False**kwargs )
Parameters
repo_id (str) — The name of the Space repo on the Hub where your tool is defined.
token (str, optional) — The token to identify you on hf.co. If unset, will use the token generated when running huggingface-cli login (stored in ~/.huggingface).
trust_remote_code(str, optional, defaults to False) — This flags marks that you understand the risk of running remote code and that you trust this tool. If not setting this to True, loading the tool from Hub will fail.
kwargs (additional keyword arguments, optional) — Additional keyword arguments that will be split in two: all arguments relevant to the Hub (such as cache_dir, revision, subfolder) will be used when downloading the files for your tool, and the others will be passed along to its init.
Loads a tool defined on the Hub.
Loading a tool from the Hub means that you’ll download the tool and execute it locally. ALWAYS inspect the tool you’re downloading before loading it within your runtime, as you would do when installing a package using pip/npm/apt.
from_langchain
<source>
( langchain_tool )
Creates a Tool from a langchain tool.
from_space
<source>
( space_id: strname: strdescription: strapi_name: str | None = Nonetoken: str | None = None ) → Tool
Parameters
space_id (str) — The id of the Space on the Hub.
name (str) — The name of the tool.
description (str) — The description of the tool.
api_name (str, optional) — The specific api_name to use, if the space has several tabs. If not precised, will default to the first available api.
token (str, optional) — Add your token to access private spaces or increase your GPU quotas.
Returns
Tool

The Space, as a tool.

Creates a Tool from a Space given its id on the Hub.

Examples:
Copied
image_generator = Tool.from_space(
    space_id="black-forest-labs/FLUX.1-schnell",
    name="image-generator",
    description="Generate an image from a prompt"
)
image = image_generator("Generate an image of a cool surfer in Tahiti")

Copied
face_swapper = Tool.from_space(
    "tuan2308/face-swap",
    "face_swapper",
    "Tool that puts the face shown on the first image on the second image. You can give it paths to images.",
)
image = face_swapper('./aymeric.jpeg', './ruth.jpg')
push_to_hub
<source>
( repo_id: strcommit_message: str = 'Upload tool'private: bool | None = Nonetoken: bool | str | None = Nonecreate_pr: bool = False )
Parameters
repo_id (str) — The name of the repository you want to push your tool to. It should contain your organization name when pushing to a given organization.
commit_message (str, optional, defaults to "Upload tool") — Message to commit while pushing.
private (bool, optional) — Whether to make the repo private. If None (default), the repo will be public unless the organization’s default is private. This value is ignored if the repo already exists.
token (bool or str, optional) — The token to use as HTTP bearer authorization for remote files. If unset, will use the token generated when running huggingface-cli login (stored in ~/.huggingface).
create_pr (bool, optional, defaults to False) — Whether to create a PR with the uploaded files or directly commit.
Upload the tool to the Hub.
save
<source>
( output_dir: str | Pathtool_file_name: str = 'tool'make_gradio_app: bool = True )
Parameters
output_dir (str or Path) — The folder in which you want to save your tool.
tool_file_name (str, optional) — The file name in which you want to save your tool.
make_gradio_app (bool, optional, defaults to True) — Whether to also export a requirements.txt file and Gradio UI.
Saves the relevant code files for your tool so it can be pushed to the Hub. This will copy the code of your tool in output_dir as well as autogenerate:
a {tool_file_name}.py file containing the logic for your tool. If you pass make_gradio_app=True, this will also write:
an app.py file providing a UI for your tool when it is exported to a Space with tool.push_to_hub()
a requirements.txt containing the names of the modules used by your tool (as detected when inspecting its code)
setup
<source>
( )
Overwrite this method here for any operation that is expensive and needs to be executed before you start using your tool. Such as loading a big model.
to_dict
<source>
( )
Returns a dictionary representing the tool
launch_gradio_demo
smolagents.launch_gradio_demo
<source>
( tool: Tool )
Parameters
tool (Tool) — The tool for which to launch the demo.
Launches a gradio demo for a tool. The corresponding tool class needs to properly implement the class attributes inputs and output_type.
ToolCollection
class smolagents.ToolCollection
<source>
( tools: list[Tool] )
Tool collections enable loading a collection of tools in the agent’s toolbox.
Collections can be loaded from a collection in the Hub or from an MCP server, see:
ToolCollection.from_hub()
ToolCollection.from_mcp()
For example and usage, see: ToolCollection.from_hub() and ToolCollection.from_mcp()
from_hub
<source>
( collection_slug: strtoken: str | None = Nonetrust_remote_code: bool = False ) → ToolCollection
Parameters
collection_slug (str) — The collection slug referencing the collection.
token (str, optional) — The authentication token if the collection is private.
trust_remote_code (bool, optional, defaults to False) — Whether to trust the remote code.
Returns
ToolCollection

A tool collection instance loaded with the tools.

Loads a tool collection from the Hub.
it adds a collection of tools from all Spaces in the collection to the agent’s toolbox
Only Spaces will be fetched, so you can feel free to add models and datasets to your collection if you’d like for this collection to showcase them.

Example:
Copied
from smolagents import ToolCollection, CodeAgent

image_tool_collection = ToolCollection.from_hub("huggingface-tools/diffusion-tools-6630bb19a942c2306a2cdb6f")
agent = CodeAgent(tools=[*image_tool_collection.tools], add_base_tools=True)

agent.run("Please draw me a picture of rivers and lakes.")
from_mcp
<source>
( server_parameters: 'mcp.StdioServerParameters' | dicttrust_remote_code: bool = Falsestructured_output: bool | None = None ) → ToolCollection
Expand 3 parameters
Parameters
server_parameters (mcp.StdioServerParameters or dict) — Configuration parameters to connect to the MCP server. This can be:

An instance of mcp.StdioServerParameters for connecting a Stdio MCP server via standard input/output using a subprocess.
A dict with at least:
“url”: URL of the server.
“transport”: Transport protocol to use, one of:
“streamable-http”: Streamable HTTP transport (default).
“sse”: Legacy HTTP+SSE transport (deprecated).
trust_remote_code (bool, optional, defaults to False) — Whether to trust the execution of code from tools defined on the MCP server. This option should only be set to True if you trust the MCP server, and undertand the risks associated with running remote code on your local machine. If set to False, loading tools from MCP will fail.
structured_output (bool, optional, defaults to False) — Whether to enable structured output features for MCP tools. If True, enables:

Support for outputSchema in MCP tools
Structured content handling (structuredContent from MCP responses)
JSON parsing fallback for structured data If False, uses the original simple text-only behavior for backwards compatibility.
Returns
ToolCollection

A tool collection instance.

Automatically load a tool collection from an MCP server.
This method supports Stdio, Streamable HTTP, and legacy HTTP+SSE MCP servers. Look at the server_parameters argument for more details on how to connect to each MCP server.
Note: a separate thread will be spawned to run an asyncio event loop handling the MCP server.

Example with a Stdio MCP server:
Copied
import os
from smolagents import ToolCollection, CodeAgent, InferenceClientModel
from mcp import StdioServerParameters

model = InferenceClientModel()

server_parameters = StdioServerParameters(
    command="uvx",
    args=["--quiet", "pubmedmcp@0.1.3"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], add_base_tools=True, model=model)
    agent.run("Please find a remedy for hangover.")

Example with structured output enabled:
Copied
with ToolCollection.from_mcp(server_parameters, trust_remote_code=True, structured_output=True) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], add_base_tools=True, model=model)
    agent.run("Please find a remedy for hangover.")

Example with a Streamable HTTP MCP server:
Copied
with ToolCollection.from_mcp({"url": "http://127.0.0.1:8000/mcp", "transport": "streamable-http"}, trust_remote_code=True) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], add_base_tools=True, model=model)
    agent.run("Please find a remedy for hangover.")
MCP Client
class smolagents.MCPClient
<source>
( server_parameters: 'StdioServerParameters' | dict[str, Any] | list['StdioServerParameters' | dict[str, Any]]adapter_kwargs: dict[str, Any] | None = Nonestructured_output: bool | None = None )
Expand 3 parameters
Parameters
server_parameters (StdioServerParameters | dict[str, Any] | list[StdioServerParameters | dict[str, Any]]) — Configuration parameters to connect to the MCP server. Can be a list if you want to connect multiple MCPs at once.

An instance of mcp.StdioServerParameters for connecting a Stdio MCP server via standard input/output using a subprocess.
A dict with at least:
“url”: URL of the server.
“transport”: Transport protocol to use, one of:
“streamable-http”: Streamable HTTP transport (default).
“sse”: Legacy HTTP+SSE transport (deprecated).
adapter_kwargs (dict[str, Any], optional) — Additional keyword arguments to be passed directly to MCPAdapt.
structured_output (bool, optional, defaults to False) — Whether to enable structured output features for MCP tools. If True, enables:

Support for outputSchema in MCP tools
Structured content handling (structuredContent from MCP responses)
JSON parsing fallback for structured data If False, uses the original simple text-only behavior for backwards compatibility.
Manages the connection to an MCP server and make its tools available to SmolAgents.
Note: tools can only be accessed after the connection has been started with the connect() method, done during the init. If you don’t use the context manager we strongly encourage to use “try … finally” to ensure the connection is cleaned up.

Example:
Copied
# fully managed context manager + stdio
with MCPClient(...) as tools:
    # tools are now available

# context manager + Streamable HTTP transport:
with MCPClient({"url": "http://localhost:8000/mcp", "transport": "streamable-http"}) as tools:
    # tools are now available

# Enable structured output for advanced MCP tools:
with MCPClient(server_parameters, structured_output=True) as tools:
    # tools with structured output support are now available

# manually manage the connection via the mcp_client object:
try:
    mcp_client = MCPClient(...)
    tools = mcp_client.get_tools()

    # use your tools here.
finally:
    mcp_client.disconnect()
connect
<source>
( )
Connect to the MCP server and initialize the tools.
disconnect
<source>
( exc_type: type[BaseException] | None = Noneexc_value: BaseException | None = Noneexc_traceback: TracebackType | None = None )
Disconnect from the MCP server
get_tools
<source>
( ) → list[Tool]
Returns
list[Tool]

The SmolAgents tools available from the MCP server.

Raises
ValueError

ValueError — If the MCP server tools is None (usually assuming the server is not started).

The SmolAgents tools available from the MCP server.
Note: for now, this always returns the tools available at the creation of the session, but it will in a future release return also new tools available from the MCP server if any at call time.
Agent Types
Agents can handle any type of object in-between tools; tools, being completely multimodal, can accept and return text, image, audio, video, among other types. In order to increase compatibility between tools, as well as to correctly render these returns in ipython (jupyter, colab, ipython notebooks, …), we implement wrapper classes around these types.
The wrapped objects should continue behaving as initially; a text object should still behave as a string, an image object should still behave as a PIL.Image.
These types have three specific purposes:
Calling to_raw on the type should return the underlying object
Calling to_string on the type should return the object as a string: that can be the string in case of an AgentText but will be the path of the serialized version of the object in other instances
Displaying it in an ipython kernel should display the object correctly
AgentText
class smolagents.AgentText
<source>
( value )
Text type returned by the agent. Behaves as a string.
AgentImage
class smolagents.AgentImage
<source>
( value )
Image type returned by the agent. Behaves as a PIL.Image.Image.
save
<source>
( output_bytesformat: str = None**params )
Parameters
output_bytes (bytes) — The output bytes to save the image to.
format (str) — The format to use for the output image. The format is the same as in PIL.Image.save.
**params — Additional parameters to pass to PIL.Image.save.
Saves the image to a file.
to_raw
<source>
( )
Returns the “raw” version of that object. In the case of an AgentImage, it is a PIL.Image.Image.
to_string
<source>
( )
Returns the stringified version of that object. In the case of an AgentImage, it is a path to the serialized version of the image.
AgentAudio
class smolagents.AgentAudio
<source>
( valuesamplerate = 16000 )
Audio type returned by the agent.
to_raw
<source>
( )
Returns the “raw” version of that object. It is a torch.Tensor object.
to_string
<source>
( )
Returns the stringified version of that object. In the case of an AgentAudio, it is a path to the serialized version of the audio.