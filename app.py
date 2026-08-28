from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from src.api.simulation_service import (

    run_simulation,

    run_recovery,

    get_latest_network_state,

    compare_recovery_strategies
)

app = Flask(__name__)


# ---------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------
@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ---------------------------------------------------
# RECOVERY DASHBOARD
# ---------------------------------------------------
@app.route("/recovery")
def recovery_dashboard():

    return render_template(
        "recovery.html"
    )


# ---------------------------------------------------
# FAILURE SIMULATION
# ---------------------------------------------------
@app.route(
    "/simulate",
    methods=["POST"]
)
def simulate():

    data = request.json

    result = run_simulation(

        failure_type=data.get(
            "failure_type"
        )
    )

    return jsonify(result)


# ---------------------------------------------------
# RECOVERY SIMULATION
# ---------------------------------------------------
@app.route(
    "/recover",
    methods=["POST"]
)
def recover():

    data = request.json

    result = run_recovery(

        recovery_type=data.get(
            "recovery_type"
        )
    )

    return jsonify(result)


# ---------------------------------------------------
# COMPARE RECOVERY STRATEGIES
# ---------------------------------------------------
@app.route(
    "/compare_recovery",
    methods=["GET"]
)
def compare_recovery():

    result = compare_recovery_strategies()

    return jsonify(result)


# ---------------------------------------------------
# CURRENT NETWORK STATE
# ---------------------------------------------------
@app.route(
    "/network_state",
    methods=["GET"]
)
def network_state():

    return jsonify(
        get_latest_network_state()
    )


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":

    app.run(
        debug=True
    )