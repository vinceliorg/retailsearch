import requests
import logging
import logging.config

logging.basicConfig(filename='/Users/vli/Work/RetailSearch/MagpieSearch/logs/embeeding.log', filemode='w', level=logging.INFO)

# create logger
logger = logging.getLogger('openai_requests')
# create console handler and set level to debug
ch = logging.StreamHandler()

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

embedding_cacahe = {}
encoder_endpoint = "https://api.openai.com/v1/embeddings"

def vectorize(text):
    logger.info(f'request info for {text}')
    if text in embedding_cacahe:
        logger.info(f'found embeeding in cache')
        return embedding_cacahe[text]
    else:
        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer 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'
        data = {
            "input": text,
            "model":"text-embedding-ada-002"
        }
        vector = []
        try:
            response = requests.post(encoder_endpoint, headers=headers, json=data)
            vector = response.json()['data'][0]['embedding']
            logger.info(f'response status {response.status_code}')
            # print(response.status_code)
        except Exception as e:
            logger.error(f'error message: {str(e)}')
            vectorize(text)
        embedding_cacahe[text] = vector
        return vector