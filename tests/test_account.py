from unittest.mock import MagicMock, patch

import pytest

from src.account import Account, AccountList, AccountManager
from src.exception import InvalidInputDataException


class TestAccount:
    def test_account_init_invalid(self):
        with pytest.raises(ValueError):
            Account(name=None, id=None)

        with pytest.raises(ValueError):
            Account(name=23423, id=2324)

    def test_account_init(self):
        account = Account(name='Test Account', id='12345')
        assert account.name == 'Test Account'
        assert account.id == '12345'

        account_dict = account.model_dump(by_alias=True)
        assert account_dict['accountName'] == 'Test Account'
        assert account_dict['accountId'] == '12345'


class TestAccountList:
    def test_account_list_invalid(self):
        with pytest.raises(ValueError):
            AccountList([{'name': 'Test Account', 'id': None}])

    def test_account_list_init(self):
        account1 = Account(name='Account 1', id='1')
        account2 = Account(name='Account 2', id='2')
        account_list = [account1, account2]

        account_list_model = AccountList.model_validate(account_list)
        assert len(account_list_model) == 2
        assert account_list_model[0].name == 'Account 1'
        assert account_list_model[1].name == 'Account 2'
        account_list_dict = account_list_model.model_dump(by_alias=True)
        assert account_list_dict[0]['accountName'] == 'Account 1'
        assert account_list_dict[1]['accountName'] == 'Account 2'

    def test_account_list_empty(self):
        empty_account_list = AccountList([])
        assert len(empty_account_list) == 0


class TestAccountManager:
    @patch('src.account.AccountManager.request.get')
    def test_get_ad_accounts(self, account_manager_request_get_mock: MagicMock):
        with pytest.raises(InvalidInputDataException):
            account_manager_request_get_mock.return_value = {}
            AccountManager.get_ad_accounts()

        with pytest.raises(InvalidInputDataException):
            account_manager_request_get_mock.return_value = {
                'invalid_key': [
                    {'id': '4d2b35432947', 'name': 'Account1'},
                    {'id': 'e38705066865', 'name': 'Account2'},
                ]
            }
            AccountManager.get_ad_accounts()

        account_manager_request_get_mock.reset_mock()
        account_manager_request_get_mock.return_value = {
            'ad_accounts': [
                {'id': '4d2b35432947', 'name': 'Account1'},
                {'id': 'e38705066865', 'name': 'Account2'},
            ]
        }
        account_list = AccountManager.get_ad_accounts()
        assert isinstance(account_list, AccountList)
        assert len(account_list) == 2
        account_manager_request_get_mock.assert_called_once_with(url='/adAccounts')
