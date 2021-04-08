import pytest

import src.minecraft_helpers.give as give
from src.minecraft_helpers.exceptions import EmptyValueException
from src.mts_utilities.mts_screen import ScreenActions

screen_name = 'm_test'


def test_give_init():
    giver = give.Give(screen_name)
    screen = ScreenActions(screen_name)
    assert giver.screen_name == screen_name
    assert type(giver.screen) == type(screen)


def test_display_prompt_success(monkeypatch):
    giver = give.Give(screen_name)
    values = ['apple', 'banana', 'cherry']
    monkeypatch.setattr('builtins.input', mock_input_1)
    giver.display_prompt(values)
    assert giver.last_selected == values[0]


def test_display_prompt_fail_index(monkeypatch):
    giver = give.Give(screen_name)
    values = ['apple', 'banana', 'cherry']
    monkeypatch.setattr('builtins.input', mock_input_7)
    with pytest.raises(IndexError):
        giver.display_prompt(values)


def test_display_prompt_fail_value(monkeypatch):
    giver = give.Give(screen_name)
    values = ['apple', 'banana', 'cherry']
    monkeypatch.setattr('builtins.input', mock_input_q)
    with pytest.raises(SystemExit):
        with pytest.raises(ValueError):
            giver.display_prompt(values)


def test_list_enchantments_success(monkeypatch):
    monkeypatch.setattr('builtins.input', mock_input_1)
    giver = give.Give(screen_name)
    item = 'bow'
    giver.list_enchantments(item)


def test_list_enchantments_fail_values(monkeypatch):
    monkeypatch.setattr('builtins.input', mock_input_1)
    giver = give.Give(screen_name)
    item = 'banana'
    with pytest.raises(EmptyValueException):
        giver.list_enchantments(item)


def test_prompt_categories_weapon(monkeypatch):
    monkeypatch.setattr('builtins.input', mock_input_1)
    giver = give.Give(screen_name)
    giver.prompt_categories()
    assert giver.last_selected == 'Bane of Arthropods'


def test_prompt_categories_armor(monkeypatch):
    monkeypatch.setattr('builtins.input', mock_input_2)
    giver = give.Give(screen_name)
    giver.prompt_categories()
    assert giver.last_selected == 'Blast Protection'


def test_prompt_categories_tools(monkeypatch):
    monkeypatch.setattr('builtins.input', mock_input_3)
    giver = give.Give(screen_name)
    giver.prompt_categories()
    assert giver.last_selected == 'Efficiency'


def test_prompt_other(monkeypatch):
    monkeypatch.setattr('builtins.input', mock_input_2)
    giver = give.Give(screen_name)
    giver.prompt_other()
    assert giver.selected_other == 'shield'
    assert giver.last_selected == 'Mending'


def test_send_command(monkeypatch):
    monkeypatch.setattr(ScreenActions, 'send', mock_screen_send)
    giver = give.Give(screen_name)
    giver.send_command()
    assert giver.command is None


def mock_input_1(something):
    return '1'


def mock_input_2(something):
    return '2'


def mock_input_3(something):
    return '3'


def mock_input_7(something):
    return '7'


def mock_input_q(something):
    return 'q'


def mock_screen_send(something, another):
    return False
