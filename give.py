#!/usr/local/bin/python3

import os

categories = ['weapon', 'armor', 'tools', 'other']

weapons = ['sword', 'bow', 'crossbow', 'trident']

head = ['helmet', 'turtle_shell']
armor = head + ['chestplate', 'pants', 'boots']

tools = ['pickaxe', 'shovel', 'axe']

extra = ['elytra', 'shield', 'fishing_rod']

all_items = armor + tools + weapons + extra

enchantments = {
    'Aqua Affinity': {
        'id': 'aqua_affinity',
        'lvl': '1',
        'items': head
    },
    'Bane of Arthropods': {
        'id': 'bane_of_arthropods',
        'lvl': '5',
        'items': [
            'sword',
            'axe'
        ]
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
        'items': all_items,
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
        'items': [
            'sword',
            'axe'
        ]
    },
    'Silk Touch': {
        'id': 'silk_touch',
        'lvl': '1',
        'items': [
                     'sword'
                 ] + tools
    },
    'Smite': {
        'id': 'smite',
        'lvl': '5',
        'items': [
            'sword',
            'axe'
        ]
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
        'items': [
            'sword',
            'axe'
        ]
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


def display_prompt(values):
    for index, value in enumerate(values, start=1):
        print('{}: {}'.format(index, value))

    value_input = input('Which would you like? ')
    return values[int(value_input) - 1]


def list_enchantments(item):
    show_enchantments = []
    for name in enchantments:
        enchantment = enchantments[name]
        items = enchantment['items']
        if item in items:
            show_enchantments.append(name)
    display_prompt(show_enchantments)


def prompt_categories():
    selected_category = display_prompt(categories)
    print('Selected category {}'.format(selected_category))

    switcher = {
        'weapon': prompt_weapons,
        'armor': prompt_armor,
        'tools': prompt_tools,
        'other': prompt_other
    }
    func = switcher.get(selected_category, 'Invalid option')
    func()


def prompt_weapons():
    selected_weapon = display_prompt(weapons)
    print('Selected weapon {}'.format(selected_weapon))
    list_enchantments(selected_weapon)


def prompt_armor():
    selected_armor = display_prompt(armor)
    print('Selected armor {}'.format(selected_armor))
    list_enchantments(selected_armor)


def prompt_tools():
    selected_tool = display_prompt(tools)
    print('Selected weapon {}'.format(selected_tool))
    list_enchantments(selected_tool)


def prompt_other():
    selected_other = display_prompt(extra)
    print('Selected armor {}'.format(selected_other))
    list_enchantments(selected_other)


def send_command():
    # send variables (screen_name, command) to the command string
    os.system("screen -r {} -X stuff {}`echo -ne '\015'`")


prompt_categories()
