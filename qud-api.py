import yaml

from flask import abort, Flask, jsonify
from flask_cors import CORS
from hagadias.gameroot import GameRoot


with open('config.yml') as f:
    config = yaml.safe_load(f)


gameroot = GameRoot(config['game_location'])
qud_object_root, qindex = gameroot.get_object_tree()
anatomies = gameroot.get_anatomies()

app = Flask(__name__)
CORS(app)


@app.route('/qud-api/objects', methods=['GET'])
def get_objects():
    return jsonify(list(qindex))


@app.route('/qud-api/objects/<object_name>', methods=['GET'])
def get_object(object_name):
    if object_name in qindex:
        return jsonify(qindex[object_name].all_attributes)
    else:
        abort(404)


@app.route('/qud-api/wearables', methods=['GET'])
def get_wearables():
    wearables = []
    for name, item in qindex.items():
        if item.wornon is not None and item.tag_BaseObject is None:
            wearables.append(name)
    return jsonify(wearables)


@app.route('/qud-api/weapons', methods=['GET'])
def get_weapons():
    weapons = []
    for name, item in qindex.items():
        if item.inherits_from('MeleeWeapon') and item.tag_BaseObject is None:
            weapons.append(name)
    return jsonify(weapons)


@app.route('/qud-api/anatomies', methods=['GET'])
def get_anatomies():
    return jsonify(anatomies)


if __name__ == '__main__':
    app.run(debug=True)
