"""All tests for mac_cleanup_py.parser"""
import pytest

from argparse import Action

from mac_cleanup.parser import Args, parser


@pytest.fixture
def get_namespace() -> Args:
    return Args()


@pytest.fixture(
    scope="session"
)
def get_parser_actions() -> list[Action]:
    action_list = parser._actions  # noqa

    # Remove help action from the list
    return action_list[1:]


def get_all_args_from_namespace(
        namespace: Args
) -> list[str]:
    """Get filtered attribute list (without dunder methods)"""

    return [attr for attr in dir(namespace) if not attr.startswith('__')]


def test_parser_description():
    from mac_cleanup.__version__ import __version__

    assert parser.description is not None and __version__ in parser.description


def test_parser_actions_empty(
        get_namespace: Args
):
    parser.parse_args(
        namespace=get_namespace
    )

    assert not any([getattr(get_namespace, attr) for attr in get_all_args_from_namespace(get_namespace)])


@pytest.mark.parametrize(
    "is_short_name",
    # test invoking actions by short and long names
    [True, False]
)
def test_parser_actions(
        is_short_name: bool,
        get_namespace: Args,
        get_parser_actions: list[Action]
):
    action_index = 0 if is_short_name else 1

    action_list = [action.option_strings[action_index] for action in get_parser_actions]

    parser.parse_args(
        args=action_list,
        namespace=get_namespace
    )

    assert all([getattr(get_namespace, attr) for attr in get_all_args_from_namespace(get_namespace)])
