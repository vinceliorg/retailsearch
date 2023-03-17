import requests
encoder_endpoint = "https://api.openai.com/v1/embeddings"
def vectorize(text):
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['Authorization'] = 'Bearer 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'
    data = {
        "input": text,
        "model":"text-embedding-ada-002"
    }
    try:
        response = requests.post(encoder_endpoint, headers=headers, json=data)
        # print(response.status_code)
    except Exception as e:
        print(e)
        vectorize(text)
    return response.json()['data'][0]['embedding']