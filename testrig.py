import numpy as np


def get_chicken_move(state):
    import numpy as np
    global info

    # info = load_info()
    info.setdefault("past-reaction-times", [])
    info.setdefault("player-behavior", {}).setdefault(state["opponent-name"], [[], []])

    if state["prev-response-time"] is not None:
        info["past-reaction-times"].append(state["prev-response-time"])
    if state["last-opponent-play"] is not None:
        info["player-behavior"][state["opponent-name"]][0].append(state["last-opponent-play"])

    past_times = info["past-reaction-times"]
    mu = np.mean(past_times)
    se = np.std(past_times)
    if len(past_times) > 10:
        time_est = mu + 1.5 * se
    else:
        time_est = 10

    oppo_moves = info["player-behavior"][state["opponent-name"]][0]
    my_moves = info["player-behavior"][state["opponent-name"]][1]

    if state["last-outcome"] == -10:
        move = 10
    elif len(oppo_moves) >= 3:
        std = np.std(oppo_moves)
        mean = np.mean(oppo_moves)
        if std < 1:
            if mean - time_est < .1 * (time_est) and mean - time_est > 0:
                move = time_est - .1 * (time_est)
            else:
                move = max(mean - time_est, time_est)
        else:
            response = oppo_moves[1:len(oppo_moves)]
            pred = my_moves[0:len(oppo_moves) - 1]
            x = np.array(pred)
            y = np.array(response)
            A = np.vstack([x, np.ones(len(x))]).T
            m, c = np.linalg.lstsq(A, y)[0]
            pred_move = my_moves[len(my_moves) - 1] * m + c
            move = max(pred_move - time_est, time_est)
    else:
        move = time_est

    move = min(max(0, move), 10)
    info["player-behavior"][state["opponent-name"]][1].append(move)
    # save_info(info)

    return {
        "move": move,
        "team-code": state["team-code"]}

def get_cx_move(state):
    return{
        "move": np.random.binomial(state[columns]-1, .5),
        "team-code": state["team-code"]
    }


def get_move(state):
    if state["game"] == "chicken":
        return get_chicken_move(state)
    else:
        return get_cx_move(state)


# test of branches...
state = {
    "game": "chicken",
    "opponent-name": "the_baddies",
    "team-code": "abc123",
    "prev-response-time": .5,
    "last-opponent-play": 1,
    "last-outcome": -10
}

info = {}
info.setdefault("past-reaction-times", [x * .1 for x in range(10)])
info.setdefault("player-behavior", {}).setdefault(state["opponent-name"], [[], []])
print(info)
for i in range(20):
    state = {
        "game": "chicken",
        "opponent-name": "the_baddies",
        "team-code": "abc123",
        "prev-response-time": .5,
        "last-opponent-play": i % 10,
        "last-outcome": -10, }
    get_chicken_move(state)
    print(info)

