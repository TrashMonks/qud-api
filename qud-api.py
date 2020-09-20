"""Simple hagadias-backed REST API for web apps.

See README.md for full API details."""
import yaml

from flask import abort, Flask, jsonify
from flask_cors import CORS
from hagadias.gameroot import GameRoot


with open('config.yml') as f:
    config = yaml.safe_load(f)

PREFIX = config['prefix']

app = Flask(__name__)
CORS(app)  # allow cross-domain loading

gameroot = GameRoot(config['game_location'])
qud_object_root, qindex = gameroot.get_object_tree()
anatomies = gameroot.get_anatomies()


@app.route(f'{PREFIX}/objects', methods=['GET'])
def get_objects():
    """Return a JSON list of all Qud object IDs."""
    return jsonify(list(qindex))


@app.route(f'{PREFIX}objects/<object_name>', methods=['GET'])
def get_object(object_name):
    """Return the full attributes (including inherited) of a Qud object."""
    if object_name not in qindex:
        abort(404)
    return jsonify(qindex[object_name].all_attributes)


@app.route(f'{PREFIX}/displayname/<object_name>', methods=['GET'])
def get_displayname(object_name):
    """Return the display name (including un-decoded color codes) of a Qud object."""
    if object_name not in qindex:
        abort(404)
    return jsonify(qindex[object_name].title)


@app.route(f'{PREFIX}/equipment', methods=['GET'])
def get_wearables():
    """Return a JSON list of equipment that can be equipped to body slots."""
    wearables = {}
    for name, item in qindex.items():
        if item.inherits_from('MeleeWeapon') and item.tag_BaseObject is None:
            wearables[name] = {'wornon': 'Hand'}
        elif item.inherits_from('Armor') and item.tag_BaseObject is None:
            wearables[name] = {'wornon': item.part_Armor_WornOn}
        if item.wornon is not None and item.tag_BaseObject is None:
            wearables[name] = {'wornon': item.wornon}
        if name in wearables and item.tag_UsesSlots:
            usesslots = item.tag_UsesSlots_Value.split(',')
            wearables[name].update({'usesslots': usesslots})

    return jsonify(wearables)


@app.route(f'{PREFIX}/weapons', methods=['GET'])
def get_weapons():
    weapons = []
    for name, item in qindex.items():
        if item.inherits_from('MeleeWeapon') and item.tag_BaseObject is None:
            weapons.append(name)
    return jsonify(weapons)


@app.route(f'{PREFIX}/anatomies', methods=['GET'])
def get_anatomies():
    return jsonify(anatomies)


if __name__ == '__main__':
    app.run(debug=True)
