import argparse, os, sys, time, requests, json

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def build_prompt(args):
    return f"Write five fundraising emails and four social captions for the {args.event} on {args.date} in a {args.tone} tone."

def gemini_completion(prompt):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        sys.exit("missing GEMINI_API_KEY")
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }
    t0 = time.time()
    url = f"{GEMINI_ENDPOINT}?key={key}"
    r = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=60)
    dt = time.time() - t0
    print(f"HTTP status: {r.status_code}")
    print("Raw response:", r.text)
    if r.status_code != 200:
        sys.exit(f"HTTP {r.status_code}: {r.text[:120]}")
    try:
        data = r.json()
    except Exception as e:
        print("Failed to decode JSON response from Gemini API.")
        print("Raw response:", r.text)
        sys.exit(f"JSON decode error: {e}")
    if not data or "candidates" not in data or not data["candidates"]:
        print("Unexpected Gemini API response format.")
        print("Raw response:", r.text)
        sys.exit("No candidates returned from Gemini API.")
    return data["candidates"][0]["content"]["parts"][0]["text"]

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
    out = gemini_completion(prompt)
    os.makedirs("out", exist_ok=True)
    with open("out/campaign.md", "w") as f:
        f.write(out)
    print(out)

if __name__ == "__main__":
    main()
