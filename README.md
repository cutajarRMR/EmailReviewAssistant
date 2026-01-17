# EmailReviewAssistant
LLM to proofread, improve, and professionalize your emails.
Choose between HuggingFace or OpenAI models.
- HuggingFace model is free (still requires a key) and uses gpt-oss-120b
- OpenAI model uses gpt-4o

## Usage
There is an input text box to paste or type your email content, and buttons to select the model: HuggingFace or OpenAI.
Press "Review Email" to get the improved email.

## Keys
Requires [HuggingFace](https://huggingface.co/settings/tokens) or [OpenAI API](https://platform.openai.com/account/api-keys) key. 
Set the environment variable HUGGINGFACE_API_KEY or OpenAI_API_KEY accordingly or have a .env file in the working area.


## Running locally
Run the python app.py, and open the index.html file in a browser.
The app runs locally at port 5050

```
start "" python app.py
start index.html
```
