from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from devopschatenginee.constraints.constants import Constants
import logging

class ChatOpsManager:

    @staticmethod
    async def start_operation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Send message on `/start`."""
        user = update.message.from_user
        logging.info("User %s started the conversation.", user.first_name)
        text = """
        Hello {name}! 👋
        Welcome to our ChatOps Bot! This friendly assistant is here to help you manage your DevOps infrastructure. Here's what you can do:

        - /start: Kick things off with this command.
        - DevOps Infrastructure button: Direct all your DevOps-related tasks like checking status, restarting services and viewing logs here.
        - Exit button: Need to leave? Use this button to exit.

        Just remember, you've got a pal to assist you. Happy managing! 😊
        """.format(name=user.first_name)

        keyboard = [
            [
                InlineKeyboardButton(text="🔧 DevOps Infrastructure", callback_data=str(Constants.COMPONENT_PICK)),
            ],
            [
                InlineKeyboardButton(text="🚪 Exit", callback_data=str(Constants.END_SESSION)),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        await update.message.reply_text(text, reply_markup=reply_markup)

        return Constants.ACTION_SELECT

    @staticmethod
    async def start_return_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        text = """
        Great to see you back! 🎉 Here's a quick reminder of what we can do together:

        - /start: Get us started.
        - DevOps Infrastructure button: Dive right into managing your DevOps infrastructure.
        - Exit button: If you need to say goodbye, use this button to exit.
        
        Remember, managing your DevOps infrastructure is a breeze when we work together! 🚀
        """
        keyboard = [
            [
                InlineKeyboardButton(text="🔧 DevOps Infrastructure", callback_data=str(Constants.COMPONENT_PICK)),
            ],
            [
                InlineKeyboardButton(text="🚪 Exit", callback_data=str(Constants.END_SESSION)),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        await query.edit_message_text(text=text, reply_markup=reply_markup)

        return Constants.ACTION_SELECT

    @staticmethod
    async def return_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        text = """
        Great to see you back! 🎉 Here's a quick reminder of what we can do together:

        - /start: Get us started.
        - DevOps Infrastructure button: Dive right into managing your DevOps infrastructure.
        - Exit button: If you need to say goodbye, use this button to exit.
        
        Remember, managing your DevOps infrastructure is a breeze when we work together! 🚀
        """
        keyboard = [
            [
                InlineKeyboardButton(text="🔧 DevOps Infrastructure", callback_data=str(Constants.COMPONENT_PICK)),
            ],
            [
                InlineKeyboardButton(text="🚪 Exit", callback_data=str(Constants.END_SESSION)),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        await query.edit_message_text(text=text, reply_markup=reply_markup)

        return Constants.ACTION_SELECT

    @staticmethod
    async def select_component(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [
                InlineKeyboardButton(text="🔹 Kubernetes", callback_data=str(Constants.COMPONENT_K8S)),
                InlineKeyboardButton(text="🔸 Gitlab", callback_data=str(Constants.COMPONENT_GITLAB)),
            ],
            [
                InlineKeyboardButton(text="🔹 Elasticsearch", callback_data=str(Constants.COMPONENT_ES)),
                InlineKeyboardButton(text="🔸 MinIO", callback_data=str(Constants.COMPONENT_MINIO)),
            ],
            [
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV)),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🎯 What's our target today? Pick the component you want to manage!", reply_markup=reply_markup
        )

        return Constants.COMPONENT_PICK

    @staticmethod
    async def select_component_return_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [
                InlineKeyboardButton(text="🔹 Kubernetes", callback_data=str(Constants.COMPONENT_K8S)),
                InlineKeyboardButton(text="🔸 Gitlab", callback_data=str(Constants.COMPONENT_GITLAB)),
            ],
            [
                InlineKeyboardButton(text="🔹 Elasticsearch", callback_data=str(Constants.COMPONENT_ES)),
                InlineKeyboardButton(text="🔸 MinIO", callback_data=str(Constants.COMPONENT_MINIO)),
            ],
            [
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV)),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🔄 Here we go again! Choose your component!", reply_markup=reply_markup
        )

        return Constants.COMPONENT_PICK
    
    @staticmethod
    async def terminate_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Returns `ConversationHandler.END`, which tells the
        ConversationHandler that the conversation is over.
        """
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="👋 It was great assisting you! Feel free to reach out anytime you need help with your Kubernetes operations. See you next time! 👋")
        
        return ConversationHandler.END