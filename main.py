import argparse, os, sys, time, requests, json
from dotenv import load_dotenv
MODEL="meta-llama/llama-4-maverick:free"
ENDPOINT="https://openrouter.ai/api/v1/chat/completions"
def build_prompt(args):
    return f"Write five fundraising emails and four social captions for the {args.event} on {args.date} in a {args.tone} tone."
def chat_completion(prompt):
    load_dotenv()
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        sys.exit("missing OPENROUTER_API_KEY in .env file")
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/",  # Required by OpenRouter
        "X-Title": "Nyla Fundraiser"  # Required by OpenRouter
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        t0 = time.time()
        r = requests.post(ENDPOINT, headers=headers, json=payload, timeout=60)
        dt = time.time() - t0
        
        print(f"Status code: {r.status_code}", file=sys.stderr)
        print(f"Response text: {r.text[:200]}", file=sys.stderr)
        
        if r.status_code != 200:
            sys.exit(f"HTTP {r.status_code}: {r.text[:120]}")
            
        print(f"done in {dt:.2f}s", file=sys.stderr)
        
        response_data = r.json()
        return response_data["choices"][0]["message"]["content"]
        
    except requests.exceptions.RequestException as e:
        sys.exit(f"Request failed: {str(e)}")
    except json.JSONDecodeError as e:
        sys.exit(f"Failed to parse JSON response: {str(e)}\nResponse text: {r.text[:200]}")
    except KeyError as e:
        sys.exit(f"Unexpected response format: {str(e)}\nResponse: {response_data}")
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--event",default="Community Gala"); p.add_argument("--date",default="TBD"); p.add_argument("--tone",default="upbeat"); p.add_argument("--dry-run",action="store_true")
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
