"""All tests for mac_cleanup_py.parser."""
from argparse import Action

import pytest

from mac_cleanup.parser import Args, parser


@pytest.fixture()
def get_namespace() -> Args:
    """Get empty args."""

    return Args()


@pytest.fixture(scope="session")
def get_parser_actions() -> list[Action]:
    """Get parser actions."""

    action_list = parser._actions  # noqa

    # Remove help action from the list
    return action_list[1:]


class TestParser:
    @staticmethod
    def get_all_args_from_namespace(namespace: Args) -> list[str]:
        """Get filtered attribute list (without dunder methods)"""

        return [attr for attr in dir(namespace) if not attr.startswith("__")]

    def test_description(self):
        """Test parser description."""

        from mac_cleanup.__version__ import __version__

        # Check current version in description
        assert parser.description is not None
        assert f"Version: {__version__}" in parser.description

    def test_actions_empty(self, get_namespace: Args):
        """Test parser without args."""

        # Set empty args to parser
        parser.parse_args(namespace=get_namespace)

        # Check there is no attrs
        assert not any(getattr(get_namespace, attr) for attr in self.get_all_args_from_namespace(get_namespace))

    @pytest.mark.parametrize(
        "is_short_name",
        # test invoking actions by short and long names
        [True, False],
    )
    def test_actions(self, is_short_name: bool, get_namespace: Args, get_parser_actions: list[Action]):
        """Test parser actions."""

        # Select actions name (short or long)
        action_index = 0 if is_short_name else 1

        # Get action list
        action_list = [action.option_strings[action_index] for action in get_parser_actions]

        # Add actions to parser
        parser.parse_args(args=action_list, namespace=get_namespace)

        # Check all attrs are set
        assert all(getattr(get_namespace, attr) for attr in self.get_all_args_from_namespace(get_namespace))
