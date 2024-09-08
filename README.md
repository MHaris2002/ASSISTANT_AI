
# Assistant AI using Groq API

This project is an AI-powered voice assistant that interacts through spoken and typed commands, using text-to-speech and speech recognition technologies. It performs various tasks based on user input, such as web searches and time inquiries. Designed for those who prefer hands-free technology and efficient information management. Ideal for users seeking a versatile and interactive tool.

***Key Features***
1. Voice Interaction
2. Text Commands
3. Web Search
4. Time Inquiry
5. Chat History Management
6. Customizable

    ***Development Environment***
1. **IDE:** The project is developed using PyCharm, a popular integrated development environment for Python.
2. **API Integration:** The Groq API is used to generate responses based on user queries.


## Environment Variables

To run this proect you will need to set groq API_KEY to authenticate your request. Here's how you can get `API_KEY`;

1. **Visit the Groq Website:** Go to the official Groq website at https://groq.com/
2. **Sign Up or Log In:** If you don’t have an account, you’ll need to sign up for one. If you already have an account, simply log in.
3. **Access `API_KEY`:** Once logged in, navigate to the Developers, then start building and here you will find API section. Click on that and generate a new `API_KEY`.
4. **Copy the Key:** Copy the `API_KEY` provided and keep it secure. You’ll need to add this key to your project’s environment variables to authenticate your requests.



## Run Locally

Open Pycharm,VScode or cmd.

Clone the project

```bash
  git clone https://github.com/MHaris2002/ASSISTANT_AI.git
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run main 

```bash
  python main.py
```
When the script is executed assistant will wait for user to say "Hey Assistant" as it is a wakeup command. Once user said that command assistant will be enabled and start talking with you.

## Feedback

If you have any feedback, please reach out to me at malikharis3984@gmail.com

