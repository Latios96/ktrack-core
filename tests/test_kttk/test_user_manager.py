import json
import os
import sys

import six
from mock import patch, MagicMock

from kttk import user_manager

INPUT = "builtins.input" if six.PY3 else "__builtin__.raw_input"


def test_get_user_information_path():
    path = user_manager.get_user_information_path()

    is_windows = sys.platform.startswith("win")
    if is_windows:
        assert path.startswith("C:")
        assert "Users" in path
    else:
        print("running not on windows, so pass this tests")


def test_generate_user_name():
    # simple test with regular strings as we expect them
    username = user_manager.generate_user_name("sonny", "black")
    assert username == "sBlack"

    # check if case is correctly converted
    username = user_manager.generate_user_name("SoSnny", "bLacK")
    assert username == "sBlack"

    # check with first name or second name is empty

    username = user_manager.generate_user_name("", "black")
    assert username == "black"

    username = user_manager.generate_user_name("sonny", "")
    assert username == "sonny"

    # check if arguments are None

    username = user_manager.generate_user_name(None, "black")
    assert username == "black"

    username = user_manager.generate_user_name("sonny", None)
    assert username == "sonny"

    username = user_manager.generate_user_name(None, None)
    assert username is None


def test_create_user():
    with patch(INPUT) as mock_raw_input:
        mock_raw_input.return_value = "sonny"

        with patch("ktrack_api.get_ktrack") as mock_kt:
            kt = MagicMock()
            kt.create.return_value = {"id": "123"}

            mock_kt.return_value = kt

            user_information = user_manager.create_user()

            kt.create.assert_called_once()
            kt.create.assert_called_with(
                "user",
                {"name": "sSonny", "first_name": "sonny", "second_name": "sonny"},
            )
            assert len(user_information.keys()) == 2
            assert user_information["type"]
            assert user_information["id"] == "123"


def test_save_user_information(tmpdir):
    # test NOT EXISTING

    # mock test dir
    with patch(
        "kttk.user_manager.get_user_information_path"
    ) as mock_user_information_path:
        user_information_path = str(tmpdir.join(".ktrack_user.json"))
        mock_user_information_path.return_value = user_information_path

        user_manager.save_user_information({"type": "user", "id": "123"})

        # json file with content {'type': 'user', 'id': '123'} exists
        os.path.isfile(user_information_path)

        with open(user_information_path, "r") as f:
            data = json.load(f)

        assert len(data.keys()) == 2
        assert data["type"] == "user"
        assert data["id"] == "123"

        # test existing override

        user_manager.save_user_information({"type": "user", "id": "456"})

        os.path.isfile(user_information_path)

        with open(user_information_path, "r") as f:
            data = json.load(f)

        assert len(data.keys()) == 2
        assert data["type"] == "user"
        assert data["id"] == "456"


def test_restore_user_not_existing(tmpdir):
    # mock test dir
    with patch(
        "kttk.user_manager.get_user_information_path"
    ) as mock_user_information_path:
        user_information_path = str(tmpdir.join(".ktrack_user.json"))
        mock_user_information_path.return_value = user_information_path

        # mock call to create_user
        with patch("kttk.user_manager.create_user") as mock_create_user:
            mock_create_user.return_value = "user"

            # mock call to save_user_information
            with patch(
                "kttk.user_manager.save_user_information"
            ) as mock_save_user_information:
                user = user_manager.restore_user()

                # does not exist, new user should be created and returns
                mock_create_user.assert_called_once()
                mock_save_user_information.assert_called_once()
                assert user == "user"


def test_restore_user_existing(tmpdir):
    # mock test dir
    with patch(
        "kttk.user_manager.get_user_information_path"
    ) as mock_user_information_path:
        user_information_path = str(tmpdir.join(".ktrack_user.json"))
        mock_user_information_path.return_value = user_information_path

        # place data
        with open(user_information_path, "w") as f:
            json.dump({"type": "user", "id": "123", "foo": "bar"}, f)

        with patch("kttk.user_manager.create_user") as mock_create_user:
            mock_create_user.return_value = "user"

            # mock call to save_user_information
            with patch(
                "kttk.user_manager.save_user_information"
            ) as mock_save_user_information:
                user = user_manager.restore_user()

                # no new user should be created and returned dict should only have two keys
                mock_create_user.assert_not_called()
                mock_save_user_information.assert_not_called()
                # validate returned user
                assert len(user.keys()) == 2
                assert user["type"] == "user"
                assert user["id"] == "123"
