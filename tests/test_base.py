from datetime import date

import pytest

from tests.mock import MockModelList


class TestBaseModelList:
    def test_init(self, mock_model_list):
        with pytest.raises(ValueError):
            MockModelList()

        obj_list = MockModelList([])
        assert isinstance(obj_list, MockModelList)
        assert len(obj_list) == 0

        assert isinstance(mock_model_list, MockModelList)
        assert len(mock_model_list) == 4

    def test_get_by_key_value(self, mock_model_list: MockModelList):
        assert mock_model_list.get_by_key_value(key='key1', value='value1') == mock_model_list[0]
        assert mock_model_list.get_by_key_value(key='key3', value='invalid_value') is None
        # Key doesn't exist
        assert mock_model_list.get_by_key_value(key='invalid_key', value='invalid_value') is None

    def test_groupby_aggregate(self, mock_model_list: MockModelList):
        # Group and Aggregate by date and string keys
        grouped = mock_model_list.groupby_aggregate(group_by=['key1', 'key3'], aggregate_by=['key2'])
        assert len(grouped) == 3
        assert grouped[0] == {'key1': 'value1', 'key3': date(2025, 4, 3), 'key2': 3}
        assert grouped[1] == {'key1': 'value2', 'key3': date(2025, 4, 3), 'key2': 3}
        assert grouped[2] == {'key1': 'value3', 'key3': date(2025, 4, 4), 'key2': 4}

        # Group and Aggregate by date only
        grouped = mock_model_list.groupby_aggregate(group_by=['key3'], aggregate_by=['key2'])
        assert len(grouped) == 2
        assert grouped[0] == {'key3': date(2025, 4, 3), 'key2': 6}
        assert grouped[1] == {'key3': date(2025, 4, 4), 'key2': 4}

        # Group and Aggregate by string keys only
        grouped = mock_model_list.groupby_aggregate(group_by=['key1'], aggregate_by=['key2'])
        assert len(grouped) == 3
        assert grouped[0] == {'key1': 'value1', 'key2': 3}
        assert grouped[1] == {'key1': 'value2', 'key2': 3}
        assert grouped[2] == {'key1': 'value3', 'key2': 4}

        # Aggregate with max function
        grouped = mock_model_list.groupby_aggregate(group_by=['key3'], aggregate_by=['key2'], agg_func=max)
        assert len(grouped) == 2
        assert grouped[0] == {'key3': date(2025, 4, 3), 'key2': 3}
        assert grouped[1] == {'key3': date(2025, 4, 4), 'key2': 4}

        # Aggregate with non existent key
        with pytest.raises(AttributeError):
            mock_model_list.groupby_aggregate(group_by=['key3'], aggregate_by=['key4'])
