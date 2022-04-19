import json

def make_replay(replay_input):
    with open("replays/replay.json", "r+") as f:
        replays = json.loads(f.read())
        replays.append(replay_input)
        f.seek(0)
        f.write(json.dumps(replays))

