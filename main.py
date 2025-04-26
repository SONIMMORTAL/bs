import argparse
import os
import sys
import time
import requests

MODEL    = "meta-llama/llama-4-maverick:free"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# ---------- helper functions ----------

def build_prompt(args) -> str:
    return (
        f"Write five fundraising emails and four social captions for "
        f"the {args.event} on {args.date} in a {args.tone} tone."
    )

def chat_completion(prompt: str) -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        sys.exit("missing OPENROUTER_API_KEY")

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }

    t0 = time.time()
    r  = requests.post(
        ENDPOINT,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type":  "application/json",
        },
        json=payload,
        timeout=60,
    )
    dt = time.time() - t0

    if r.status_code != 200:
        sys.exit(f"HTTP {r.status_code}: {r.text[:120]}")
    print(f"done in {dt:.2f}s", file=sys.stderr)

    return r.json()["choices"][0]["message"]["content"]

# ---------- CLI entrypoint ----------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate fundraising copy via OpenRouter"
    )
    parser.add_argument("--event",   default="Community Gala",
                        help="Name of the fundraising event")
    parser.add_argument("--date",    default="TBD",
                        help="Event date, e.g. 2025-05-30")
    parser.add_argument("--tone",    default="upbeat",
                        help="Copy voice (upbeat, formal, humorous, etc.)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the prompt and exit")
    parser.add_argument("--outfile", default="out/campaign.md",
                        help="Where to write the generated markdown")

    args = parser.parse_args()              # ← parse *after* all flags defined
    prompt = build_prompt(args)

    if args.dry_run:                        # fast-fail branch
        print(prompt)
        return

    output = chat_completion(prompt)

    os.makedirs(os.path.dirname(args.outfile), exist_ok=True)
    with open(args.outfile, "w") as f:
        f.write(output)

    print(output)

if __name__ == "__main__":
    main()
