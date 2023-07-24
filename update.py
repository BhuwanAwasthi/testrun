import requests
import json
import base64

def fetch_and_parse_json(url):
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as error:
        print("Error fetching and parsing JSON:", error)
        return None

def update_github_repo():
    first_data = fetch_and_parse_json("https://raw.githubusercontent.com/scamsniffer/scam-database/main/blacklist/domains.json")
    second_data = fetch_and_parse_json("https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/main/src/config.json")

    if first_data and second_data:
        blacklist = second_data["blacklist"]

        # Fetch the existing domains.json file from the repository
        target_url = 'https://api.github.com/repos/BeastEth/blacklist/contents/domains.json'
        auth_token = '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'

        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response_target = requests.get(target_url, headers=headers)
        target_data = response_target.json()

        if 'content' in target_data:
            existing_content = base64.b64decode(target_data['content']).decode()
            try:
                existing_domains = json.loads(existing_content)
            except json.JSONDecodeError:
                existing_domains = []
        else:
            existing_domains = []

        updated_domains = list(set(first_data + blacklist + existing_domains))

        # Convert the updated content to JSON format
        updated_content = json.dumps(updated_domains)

        # Create a commit payload
        commit_message = "Update domains.json"
        commit_payload = {
            "message": commit_message,
            "content": base64.b64encode(updated_content.encode()).decode(),
            "sha": target_data['sha']
        }

        # Make a PUT request to update the target JSON file on GitHub
        response_update = requests.put(target_url, headers=headers, data=json.dumps(commit_payload))

        if response_update.status_code == 200:
            print("JSON file updated successfully.")
        else:
            print("Failed to update JSON file.")

def main():
    # Update GitHub repository with combined domain names
    update_github_repo()

if __name__ == "__main__":
    main()
