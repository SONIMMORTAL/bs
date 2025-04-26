import argparse, os, sys, time, requests, json
MODEL="meta-llama/llama-4-maverick:free"
ENDPOINT="https://openrouter.ai/api/v1/chat/completions"
def build_prompt(args):
    return f"Write five fundraising emails and four social captions for the {args.event} on {args.date} in a {args.tone} tone."
def chat_completion(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-repo",  # Replace with your actual repo URL
        "X-Title": "Fundraising Email Generator"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        response.raise_for_status()
        
        try:
            return response.json()["choices"][0]["message"]["content"]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing response: {e}")
            print(f"Response content: {response.text[:500]}...")
            raise
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text[:500]}...")
        raise
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--event",default="Community Gala"); p.add_argument("--date",default="2025-05-30"); p.add_argument("--tone",default="enthusiastic and heartfelt"); p.add_argument("--dry-run",action="store_true")
    a=p.parse_args()
    prompt=build_prompt(a)
    if a.dry_run:
        print(prompt); return
    out=chat_completion(prompt)
    os.makedirs("out",exist_ok=True)
    with open("out/campaign.md","w") as f: f.write(out)
    print(out)
if __name__=="__main__":
    main()
