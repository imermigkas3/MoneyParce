
from plaid import Configuration, ApiClient
from plaid.api import plaid_api
from config import PLAID_SECRET, PLAID_CLIENT_ID

configuration = Configuration(
    host="https://sandbox.plaid.com",
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

