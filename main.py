from devopschatenginee.utils.logger_setup import LoggerSetup
from devopschatenginee.states.chat_states import ChatStates

from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import (
    Application,
    ConversationHandler,
)

class App:
    def main() -> None:
        # Set up logging
        LoggerSetup.setup_logging()

        """Run the bot."""
        # Create the Application and pass it your bot's token.
        # This will instantiate your bot and provide it with its authentication token
        application = Application.builder().token("5782352916:AAFDwKZaYhhQsH2oK3bk54oO0_Cz2kcjEdg").build()

        # Define a conversation handler, which will manage dialogue flow between the bot and the user
        # This handler will transition between different states according to user input

        conv_handler = ConversationHandler(
            # "start" command triggers the start_operation function
            entry_points=ChatStates.get_entry_points(),
            # States represent the different stages of the conversation, where each stage is associated with a list of handlers
            states=ChatStates.get_states(),
            # If any other input is given in any state, fallbacks will handle it
            fallbacks=ChatStates.get_fallbacks(),
        )

        # Add ConversationHandler to application that will be used for handling updates
        application.add_handler(conv_handler)

        # Run the bot until the user presses Ctrl-C
        # Polling method is used to get updates from the Telegram server
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    App.main()