import os
import time
from dotenv import load_dotenv
import anthropic

# Load API key from .env file
load_dotenv()
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# List of Claude Sonnet models to test
# models = [
#     "claude-3-sonnet-20240229",     # Legacy Sonnet
#     "claude-3-5-sonnet-20241022",   # Claude 3.5 Sonnet
#     "claude-3-7-sonnet-20250219",   # Claude 3.7 Sonnet (latest)
# ]
# List of Claude Haiku models to test
models = [
    "claude-3-5-haiku-20241022",  # Claude 3.5 Haiku (latest)
    "claude-3-haiku-20240307",    # Claude 3 Haiku (legacy)
]

test_prompt = "Explain how machine learning works in simple terms."

# Function to test a model and return its output and timing
def test_model(model: str, prompt: str):
    start_time = time.time()
    
    # Send prompt via Anthropic Messages API
    response = client.messages.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0.0,
    )

    elapsed_time = time.time() - start_time
    response_text = response.content[0].text
    # response_text = response.content.strip()

    return response_text, elapsed_time

# Iterate through each model, test it, and save to a file
for model_name in models:
    print(f"Testing model: {model_name}")
    output, duration = test_model(model_name, test_prompt)
    
    # Define the output filename
    safe_model_name = model_name.replace('/', '_')  # In case of slashes
    filename = f"{safe_model_name}_output.txt"
    
    # Write the results to the file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Model: {model_name}\n")
        file.write(f"Response Time: {duration:.2f} seconds\n\n")
        file.write(output)

    print(f"Saved output to {filename}\n")
    # Throttle requests to avoid rate limits
    time.sleep(1)
