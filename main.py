import boto3
import csv
import logging
import json

def traverse_ou(org_units, account_ou_map, current_path=""):
    for ou in org_units:
        ou_path = current_path + "/" + ou['Name'] if current_path else ou['Name']
        accounts = client.list_accounts_for_parent(ParentId=ou['Id'])['Accounts']
        for account in accounts:
            account_ou_map[account['Id']] = ou_path
        
        children = client.list_organizational_units_for_parent(ParentId=ou['Id'])['OrganizationalUnits']
        traverse_ou(children, account_ou_map, ou_path)

# Configure logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace this with your list of account numbers
account_numbers = ['123456789012', '234567890123', '345678901234', '123456789012']

# Remove duplicate account numbers
account_numbers = list(set(account_numbers))

# Initialize AWS Organizations client
client = boto3.client('organizations')

# Initialize output list
output = []

# Get the organization's root and list of OUs
root = client.list_roots()['Roots'][0]
org_units = client.list_organizational_units_for_parent(ParentId=root['Id'])['OrganizationalUnits']

# Traverse OU structure and store account to OU mapping
account_ou_map = {}
traverse_ou(org_units, account_ou_map)

def main():
    # Get account details
    for account_number in account_numbers:
        try:
            account = client.describe_account(AccountId=account_number)['Account']
        except client.exceptions.AccountNotFoundException:
            logging.error(f"Account not found: {account_number}")
            continue

        # Get OU of the account
        ou_path = account_ou_map.get(account_number)
        if ou_path is None:
            logging.warning(f"OU not found for account: {account_number}")

        # Get account tags
        try:
            tags = client.list_tags_for_resource(ResourceId=account['Id'])['Tags']
        except Exception as e:
            logging.error(f"Error fetching tags for account {account_number}: {e}")
            tags = []

        tags_dict = {tag['Key']: tag['Value'] for tag in tags}
        owner_name = tags_dict.get('OwnerName')
        route_domain = tags_dict.get('route-domain')
        environment = tags_dict.get('Environment')

        # Append account info to output list
        output.append({
            'AccountNumber': int(account_number),
            'AccountName': account['Name'],
            'OUPath': ou_path,
            'OwnerName': owner_name,
            'RouteDomain': route_domain,
            'Environment': environment
        })

    # Pretty-print output to screen
    print(json.dumps(output, indent=2))

def csvoutput():
    # Write output to CSV
    with open('aws_accounts.csv', 'w', newline='') as csvfile:
        fieldnames = ['AccountNumber', 'AccountName', 'OUPath', 'OwnerName', 'RouteDomain', 'Environment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in output:
            writer.writerow(row)

        
if __name__ == '__main__':
    main()
    csvoutput()
