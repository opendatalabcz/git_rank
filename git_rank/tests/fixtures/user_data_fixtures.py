import pytest

from git_rank.models.user_data import UserData

TEST_USERNAME = "TEST_USERNAME"
TEST_USER_NAME = "TEST_USER_NAME"
TEST_USER_EMAIL = "TEST_USER_EMAIL"


@pytest.fixture(name="user_data_fixture")
def user_data_fixture() -> UserData:
    return UserData(
        username=TEST_USERNAME,
        user_name=TEST_USER_NAME,
        user_email=TEST_USER_EMAIL,
    )
