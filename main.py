import argparse, os, sys
from openai import OpenAI

MODEL = "meta-llama/llama-4-maverick:free"
ENDPOINT = "https://openrouter.ai/api/v1"
REFERER = "http://localhost"
TITLE = "Nyla Fundraiser Copy CLI"

def get_api_key():
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        # Try to read from a file in the project directory
        try:
            with open("openrouter_api_key.txt") as f:
                key = f.read().strip()
        except FileNotFoundError:
            sys.exit("missing OPENROUTER_API_KEY and openrouter_api_key.txt")
    return key

def build_prompt(args):
    return f"Write five fundraising emails and four social captions for the {args.event} on {args.date} in a {args.tone} tone."

def chat_completion(prompt):
    key = get_api_key()
    client = OpenAI(base_url=ENDPOINT, api_key=key)
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": REFERER,
            "X-Title": TITLE,
        },
        extra_body={},
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--event", default="Community Gala")
    p.add_argument("--date", default="TBD")
    p.add_argument("--tone", default="upbeat")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    prompt = build_prompt(a)
    if a.dry_run:
        print(prompt)
        return
    out = chat_completion(prompt)
    os.makedirs("out", exist_ok=True)
    with open("out/campaign.md", "w") as f:
        f.write(out)
    print(out)

if __name__ == "__main__":
    main()
