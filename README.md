# Telegram GIF Searcher Bot
### Made with [Oleksandr Orlov](https://github.com/orlovol) - using this [repo](https://github.com/orlovol/deta-tg-bot) as example

This repository contains a FastAPI-based web application that functions as a Telegram bot for searching and sharing GIFs using the Giphy API. The bot interacts with users through Telegram messages and responds with GIFs based on user prompts. It features the following functionalities:

1. **Webhook Setup**: The bot can be set up to use a webhook to receive messages from Telegram. It provides endpoints for setting up and removing the webhook.

2. **GIF Searching**: Users can send a text prompt to the bot, and it will search the Giphy API for GIFs related to the prompt. If GIFs are found, the bot responds with a link to the first GIF. If no matching GIFs are found, it provides an appropriate message.

3. **Commands**: The bot responds to commands like `"/start"` and `"/stop"`. The `"/start"` command provides a welcome message and instructions, while the `"/stop"` command bids farewell to the user.

4. **Messaging**: The bot can send messages to users with GIF search results, prompts, and instructions.

Deploying on platform [![Deta Space](https://img.shields.io/badge/Deta-Space-ff69b4?logo=deta)](https://deta.space/your-project-name)

