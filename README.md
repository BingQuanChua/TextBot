# TextBot
A sentiment analysis Discord bot build with spaCy and TextBlob during MMU Hackerspace Hackathon 2021!



## Guide to Running TextBot Locally

1. Create a new application on [Discord Developer Portal](https://discord.com/developers/applications). Create a bot and copy the token. Invite the bot to one of your servers too.

2. Clone this repository.

3. Create a `.env` file in the same directory and paste your token.

   ```
   TOKEN=<token>
   ```

4. Install the spaCy library along with the English language model.

   ```
   $ pip install spacy
   $ python -m spacy download en_core_web_sm
   ```

5. Install spacytextblob, which is basically spaCy + Textblob. This adds Textblob to the last step of the spaCy nlp pipline.

   ```
   $ pip install spacytextblob   
   $ python -m textblob.download_corpora
   ```

6. Install svglib, which allows Python to read `.svg` files and convert them into `.png`. 

   [Optional] Install python-decouple for reading environmental variables (for secret bot token).

   ```
   $ pip install svglib
   $ pip install python-decouple 
   ```

7. Run the bot. The bot should now be online. 

