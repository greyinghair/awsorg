import boto3
import csv
import logging

# Configure logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace this with your list of account numbers
account_numbers = ['123456789012', '234567890123', '345678901234']

# Initialize AWS Organizations client
client = boto3.client('organizations')

# Initialize output list
output = []

# Get the organization's root and list of OUs
root = client.list_roots()['Roots'][0]
org_units = client.list_organizational_units_for_parent(ParentId=root['Id'])['OrganizationalUnits']

def main():
    # Get account details
    for account_number in account_numbers:
        try:
            account = client.describe_account(AccountId=account_number)['Account']
        except client.exceptions.AccountNotFoundException:
            logging.error(f"Account not found: {account_number}")
            continue

        # Get OU of the account
        ou_name = None
        for ou in org_units:
            accounts = client.list_accounts_for_parent(ParentId=ou['Id'])['Accounts']
            if any(a['Id'] == account_number for a in accounts):
                ou_name = ou['Name']
                break

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
            'AccountNumber': account_number,
            'AccountName': account['Name'],
            'OU': ou_name,
            'OwnerName': owner_name,
            'RouteDomain': route_domain,
            'Environment': environment
        })

    # Print output and write to CSV
    print(output)

with open('aws_accounts.csv', 'w', newline='') as csvfile:
    fieldnames = ['AccountNumber', 'AccountName', 'OU', 'OwnerName', 'RouteDomain', 'Environment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in output:
        writer.writerow(row)
        
 if __name__ == '__main__':
    main()
