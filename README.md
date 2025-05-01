# MoneyParce

MoneyParce is a web application used to aid in organizing personal finances. The tools it includes allows users to input their income and spending, categorizes their spending and sets budgets. It also provides tips and reports to show the user how they can improve their money management. MoneyParce will integrate APIs for users to organize all their finances including Plaid API for tracking these finances by connecting to banks, Google Charts API for creating graphs and reports, and Gemini API calls for generating tips.

The website is deployed using Render and can be accessed at: https://moneyparce-7etg.onrender.com/

For security, personal API keys have been removed, and as a result running parts of the app (Chatbot Agent, linking to Bank Accounts with Plaid) requires these to be added to the config.py file found in the main directory of the GitHub, which can be done after cloning the repository.
