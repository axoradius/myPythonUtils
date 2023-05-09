import myConfig
import openai

openai.api_key = myConfig.getApiKey()
prompt = "draw a house with swimming pool"

response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256",
)
print(response["data"][0]["url"])