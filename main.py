import argparse
import json
import os
import sys
import time
import requests

# Constants
MODEL = "meta-llama/llama-4-maverick:free"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

def build_prompt(args: argparse.Namespace) -> str:
    """Build a prompt based on user arguments."""
    if args.custom_prompt:
        return args.custom_prompt
    
    # Build the count string based on what we're generating
    count = f"{args.email_count} fundraising emails" if not args.social_only else ""
    social_count = f"{args.social_count} social captions" if not args.emails_only else ""
    
    if count and social_count:
        count = f"{count} and {social_count}"
    elif social_count:
        count = social_count
    
    return f"Write {count} for the {args.event} on {args.date} in a {args.tone} tone. {args.additional_context}"

def chat_completion(prompt: str, temperature: float = 0.7) -> str:
    """Send a prompt to the LLM and get a response."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        sys.exit("Error: OPENROUTER_API_KEY environment variable is not set. Please set it and try again.")
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    
    print(f"Sending request to {MODEL}...", file=sys.stderr)
    t0 = time.time()
    
    try:
        r = requests.post(
            ENDPOINT,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )
        r.raise_for_status()
    except requests.exceptions.Timeout:
        sys.exit("Error: Request timed out. Please try again later.")
    except requests.exceptions.HTTPError as e:
        sys.exit(f"HTTP Error: {e.response.status_code} - {e.response.text[:200]}")
    except requests.exceptions.RequestException as e:
        sys.exit(f"Request Error: {str(e)}")
    
    dt = time.time() - t0
    print(f"Response received in {dt:.2f}s", file=sys.stderr)
    
    # Debugging information for troubleshooting
    try:
        if not r.text.strip():
            sys.exit("Error: Received empty response from API")
        
        response_data = r.json()
        print(f"Response status code: {r.status_code}", file=sys.stderr)
        
        if "choices" not in response_data or not response_data["choices"]:
            print(f"API response: {json.dumps(response_data, indent=2)[:500]}", file=sys.stderr)
            sys.exit("Error: API response is missing the 'choices' field")
        
        choice = response_data["choices"][0]
        if "message" not in choice or "content" not in choice["message"]:
            print(f"Choice data: {json.dumps(choice, indent=2)}", file=sys.stderr)
            sys.exit("Error: API response has an unexpected format")
        
        return choice["message"]["content"]
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response. Raw response: {r.text[:500]}", file=sys.stderr)
        sys.exit(f"Error parsing JSON response: {str(e)}")
    except (KeyError, IndexError) as e:
        print(f"Response structure issue. Response: {r.text[:500]}", file=sys.stderr)
        sys.exit(f"Error extracting data from response: {str(e)}")
    except Exception as e:
        sys.exit(f"Unexpected error processing response: {str(e)}")

def list_models() -> None:
    """List available models from OpenRouter."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        sys.exit("Error: OPENROUTER_API_KEY environment variable is not set. Please set it and try again.")
    
    try:
        r = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {key}"}
        )
        r.raise_for_status()
        models = r.json()
        
        print("Available models:")
        for model in models.get("data", []):
            name = model.get("id", "Unknown")
            context_length = model.get("context_length", "Unknown")
            print(f"- {name} (Context length: {context_length})")
    except Exception as e:
        sys.exit(f"Error listing models: {str(e)}")

def main() -> None:
    """Main entry point for the CLI."""
    global MODEL
    
    parser = argparse.ArgumentParser(
        description="Generate fundraising emails and social media content using AI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Campaign details
    parser.add_argument("--event", default="Community Gala", help="Name of the event or campaign")
    parser.add_argument("--date", default="TBD", help="Date of the event")
    parser.add_argument("--tone", default="upbeat", help="Tone for the content (e.g., upbeat, formal, urgent)")
    parser.add_argument("--additional-context", default="", help="Additional context or requirements to include")
    
    # Content options
    parser.add_argument("--emails-only", action="store_true", help="Generate only fundraising emails")
    parser.add_argument("--social-only", action="store_true", help="Generate only social media captions")
    parser.add_argument("--email-count", type=int, default=5, help="Number of fundraising emails to generate")
    parser.add_argument("--social-count", type=int, default=4, help="Number of social captions to generate")
    
    # Model options
    parser.add_argument("--model", default=MODEL, help="Model to use for generation")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation (0.1-1.0)")
    parser.add_argument("--list-models", action="store_true", help="List available models and exit")
    
    # Output options
    parser.add_argument("--output", default="out/campaign.md", help="Output file path")
    parser.add_argument("--custom-prompt", help="Use a custom prompt instead of the built-in template")
    parser.add_argument("--dry-run", action="store_true", help="Show the prompt without sending to the API")
    
    args = parser.parse_args()
    
    # Handle list models request
    if args.list_models:
        list_models()
        return
    
    # Update model if specified
    MODEL = args.model
    
    # Build the prompt
    prompt = build_prompt(args)
    
    # Handle dry run
    if args.dry_run:
        print("Prompt that would be sent:")
        print(prompt)
        return
    
    # Get the completion
    out = chat_completion(prompt, args.temperature)
    
    # Save the output
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(args.output, "w") as f:
        f.write(out)
    
    print(f"Output saved to {args.output}")
    print("\n" + out)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
