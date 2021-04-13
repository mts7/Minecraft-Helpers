import sys

from src.minecraft_helpers.exceptions import EmptyValueException
from src.mts_utilities.mts_screen import ScreenActions


class Give:
    """Module to generate a string to send to a Minecraft server.

    This goes through a series of prompts to determine which items and
    enchantments are desired, then displays the give command.

    ```python
    python3 -m src.give
    ```
    """
    # set these in the constructor
    screen_name = 'minecraft'

    # class properties
    # The following are the items listed by the prompt.
    categories = ['weapon', 'armor', 'tools', 'other']
    weapons = ['sword', 'bow', 'crossbow', 'trident']
    head = ['helmet', 'turtle_shell']
    armor = [*head, 'chestplate', 'leggings', 'boots']
    tools = ['pickaxe', 'shovel', 'axe', 'hoe', 'shears']
    extra = ['elytra', 'shield', 'fishing_rod']
    all_items = [*armor, *tools, *weapons, *extra]
    pointy_items = ['sword', 'axe']

    # These are the available enchantments and their enchantable items.
    enchantments = {
        'Aqua Affinity': {
            'id': 'aqua_affinity',
            'lvl': '1',
            'items': head
        },
        'Bane of Arthropods': {
            'id': 'bane_of_arthropods',
            'lvl': '5',
            'items': pointy_items
        },
        'Blast Protection': {
            'id': 'blast_protection',
            'lvl': '4',
            'items': armor
        },
        'Channeling': {
            'id': 'channeling',
            'lvl': '1',
            'items': [
                'trident'
            ]
        },
        'Curse of Binding': {
            'id': 'binding_curse',
            'lvl': '1',
            'items': armor,
        },
        'Curse of Vanishing': {
            'id': 'vanishing_curse',
            'lvl': '1',
            'items': all_items,
        },
        'Depth Strider': {
            'id': 'depth_strider',
            'lvl': '3',
            'items': [
                'boots'
            ]
        },
        'Efficiency': {
            'id': 'efficiency',
            'lvl': '5',
            'items': tools
        },
        'Feather Falling': {
            'id': 'feather_falling',
            'lvl': '4',
            'items': [
                'boots'
            ]
        },
        'Fire Aspect': {
            'id': 'fire_aspect',
            'lvl': '2',
            'items': [
                'sword'
            ]
        },
        'Fire Protection': {
            'id': 'fire_protection',
            'lvl': '4',
            'items': armor
        },
        'Flame': {
            'id': 'flame',
            'lvl': '1',
            'items': [
                'bow'
            ]
        },
        'Fortune': {
            'id': 'fortune',
            'lvl': '3',
            'items': tools
        },
        'Frost Walker': {
            'id': 'frost_walker',
            'lvl': '2',
            'items': [
                'boots'
            ]
        },
        'Impaling': {
            'id': 'impaling',
            'lvl': '5',
            'items': [
                'trident'
            ]
        },
        'Infinity': {
            'id': 'infinity',
            'lvl': '1',
            'items': [
                'bow'
            ]
        },
        'Knockback': {
            'id': 'knockback',
            'lvl': '2',
            'items': [
                'sword'
            ]
        },
        'Looting': {
            'id': 'looting',
            'lvl': '3',
            'items': [
                'sword'
            ]
        },
        'Loyalty': {
            'id': 'loyalty',
            'lvl': '3',
            'items': [
                'trident'
            ]
        },
        'Luck of the Sea': {
            'id': 'luck_of_the_sea',
            'lvl': '3',
            'items': [
                'fishing_rod'
            ]
        },
        'Lure': {
            'id': 'lure',
            'lvl': '3',
            'items': [
                'fishing_rod'
            ]
        },
        'Mending': {
            'id': 'mending',
            'lvl': '1',
            'items': all_items
        },
        'Multishot': {
            'id': 'multishot',
            'lvl': '1',
            'items': [
                'crossbow'
            ]
        },
        'Piercing': {
            'id': 'piercing',
            'lvl': '4',
            'items': [
                'crossbow'
            ]
        },
        'Power': {
            'id': 'power',
            'lvl': '5',
            'items': [
                'bow'
            ]
        },
        'Projectile Protection': {
            'id': 'projectile_protection',
            'lvl': '4',
            'items': armor
        },
        'Punch': {
            'id': 'punch',
            'lvl': '2',
            'items': [
                'bow'
            ]
        },
        'Quick Charge': {
            'id': 'quick_charge',
            'lvl': '3',
            'items': [
                'crossbow'
            ]
        },
        'Respiration': {
            'id': 'aqua_affinity',
            'lvl': '3',
            'items': head
        },
        'Riptide': {
            'id': 'riptide',
            'lvl': '3',
            'items': [
                'trident'
            ]
        },
        'Sharpness': {
            'id': 'sharpness',
            'lvl': '5',
            'items': pointy_items
        },
        'Silk Touch': {
            'id': 'silk_touch',
            'lvl': '1',
            'items': [
                'sword',
                *tools
            ]
        },
        'Smite': {
            'id': 'smite',
            'lvl': '5',
            'items': pointy_items
        },
        'Soul Speed': {
            'id': 'soul_speed',
            'lvl': '3',
            'items': [
                'boots'
            ]
        },
        'Sweeping Edge': {
            'id': 'sweeping',
            'lvl': '3',
            'items': pointy_items
        },
        'Thorns': {
            'id': 'thorns',
            'lvl': '3',
            'items': armor
        },
        'Unbreaking': {
            'id': 'unbreaking',
            'lvl': '3',
            'items': all_items
        }
    }

    # instance variables
    command = None
    last_selected = None
    selected_armor = None
    selected_category = None
    selected_other = None
    selected_tool = None
    selected_weapon = None

    def __init__(self, screen_name: str = 'minecraft'):
        self.screen_name = screen_name
        self.screen = ScreenActions(screen_name)

    def display_prompt(self, values: list):
        """Displays a prompt with the passed values and sets the input value.

        Parameters
        ----------
        values : list
            Values to display
        """
        if values is None or values == []:
            raise EmptyValueException('values')

        for index, value in enumerate(values, start=1):
            print('{}: {}'.format(index, value))

        value_input = input('Which would you like? ')
        try:
            self.last_selected = values[int(value_input) - 1]
        except ValueError:
            print('exiting')
            sys.exit(0)

    def list_enchantments(self, item: str):
        """List the enchantments in a prompt based on the item passed.

        Parameters
        ----------
        item : str
            Item to enchant
        """
        show_enchantments = []
        for name in self.enchantments:
            enchantment = self.enchantments[name]
            items = enchantment['items']
            if item in items:
                show_enchantments.append(name)
        self.display_prompt(show_enchantments)

    def prompt_categories(self):
        """Display a prompt for categories."""
        self.display_prompt(self.categories)
        self.selected_category = self.last_selected
        print('Selected category {}'.format(self.selected_category))

        switcher = {
            'weapon': self.prompt_weapons,
            'armor': self.prompt_armor,
            'tools': self.prompt_tools,
            'other': self.prompt_other
        }
        func = switcher.get(self.selected_category, 'Invalid option')
        func()

    def prompt_weapons(self):
        """Display a prompt for weapons."""
        self.display_prompt(self.weapons)
        self.selected_weapon = self.last_selected
        print('Selected weapon {}'.format(self.selected_weapon))
        self.list_enchantments(self.selected_weapon)

    def prompt_armor(self):
        """Display a prompt for armor."""
        self.display_prompt(self.armor)
        self.selected_armor = self.last_selected
        print('Selected armor {}'.format(self.selected_armor))
        self.list_enchantments(self.selected_armor)

    def prompt_tools(self):
        """Display a prompt for tools."""
        self.display_prompt(self.tools)
        self.selected_tool = self.last_selected
        print('Selected weapon {}'.format(self.selected_tool))
        self.list_enchantments(self.selected_tool)

    def prompt_other(self):
        """Display a prompt for other."""
        self.display_prompt(self.extra)
        self.selected_other = self.last_selected
        print('Selected other {}'.format(self.selected_other))
        self.list_enchantments(self.selected_other)

    def send_command(self):
        """Send the command to the screen instance."""
        # send variables (screen_name, command) to the command string
        self.screen.send(self.command)
