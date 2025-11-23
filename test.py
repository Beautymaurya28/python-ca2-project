from google import genai

client = genai.Client(api_key="AIzaSyCwc59gNKsqC_HCBYt0Ez_fHkRel4M7Wgs")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words"
)

print(response.text)