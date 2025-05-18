#You have to buy this api key to allow OpenAi to answer question other than set one. for pay(https://platform.openai.com/settings/organization/billing/overview)of 5 dollar.If you pay then first test the program here than on main.py , the code i have integrated it with program already.
from openai import OpenAI

client = OpenAI(
    api_key = API KEY,
)

response = client.responses.create(
    model="gpt-4.1",
    input="Write about recursive function in c language."
)

print(response.output_text)

