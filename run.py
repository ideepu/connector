import argparse
import random
import sys
from datetime import date, timedelta

from src.connector import Connector
from src.exception import CoreException

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sultek advertising platform connector')
    parser.add_argument('--ad_account_id', type=str, help='Ad account ID', required=False)
    parser.add_argument(
        '--start',
        type=date.fromisoformat,
        help='Start date (optional): If not provided, a random date between 30 and 60 days ago will be selected.',
        required=False,
    )
    parser.add_argument(
        '--end',
        type=date.fromisoformat,
        help='End date (optional): If not specified, a random date between the start date and up to 30 days after will be selected.',
        required=False,
    )
    args = parser.parse_args()

    ad_account_id = args.ad_account_id
    # Select random dates if not provided
    # Start date ranges from 30 to 60 days ago (older date)
    # End date is between the start date and 30 days after it (more recent date)
    start = args.start or date.today() - timedelta(days=random.randint(30, 60))
    end = args.end or start + timedelta(days=random.randint(0, 30))
    try:
        Connector(account_id=ad_account_id, start=start, end=end).run()
    except CoreException as e:
        print(e)
        sys.exit(1)
