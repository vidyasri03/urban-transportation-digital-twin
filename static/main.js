let map = L.map('map').setView(
    [17.0, 81.8],
    13
);

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        maxZoom: 19
    }
).addTo(map);

let markers = [];


// ----------------------------------------------------
// NODE COLOR
// ----------------------------------------------------
function getColor(node) {

    if (node.status === "failed")
        return "red";

    if (node.status === "congested")
        return "orange";

    return "#157d47";
}


// ----------------------------------------------------
// DRAW NODES
// ----------------------------------------------------
function drawNodes(nodes) {

    markers.forEach(
        m => map.removeLayer(m)
    );

    markers = [];

    nodes.forEach(node => {

        let marker = L.circleMarker(

            [node.lat, node.lon],

            {
                radius: 6,

                color: getColor(node),

                fillColor: getColor(node),

                fillOpacity: 0.9,

                weight: 0
            }

        ).addTo(map);

        marker.bindPopup(`

            <b>Node ${node.id}</b><br>

            Status:
            ${node.status}<br>

            Load:
            ${node.load.toFixed(2)}
            /
            ${node.capacity.toFixed(2)}
            <br>

            Utilization:
            ${(
                node.load /
                node.capacity *
                100
            ).toFixed(1)}%
            <br><br>

            Importance:
            ${node.importance.toFixed(4)}
            <br>

            Betweenness:
            ${node.betweenness.toFixed(4)}
            <br>

            Eigenvector:
            ${node.eigenvector.toFixed(4)}

        `);

        markers.push(marker);
    });
}


// ----------------------------------------------------
// FAILURE SIMULATION
// ----------------------------------------------------
function runSimulation(type) {

    fetch('/simulate', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({

            failure_type: type
        })
    })

    .then(res => res.json())

    .then(data => {

        // ----------------------------------------
        // DRAW MAP
        // ----------------------------------------
        drawNodes(data.nodes);

        // ----------------------------------------
        // METRICS
        // ----------------------------------------
        document.getElementById(
            "active"
        ).innerText =

            data.nodes.length -
            data.failed_nodes.length;

        document.getElementById(
            "failed"
        ).innerText =

            data.failed_nodes.length;

        document.getElementById(
            "eff"
        ).innerText =

            data.after_metrics
            .Efficiency
            .toFixed(4);

        document.getElementById(
            "loss"
        ).innerText =

            data.after_metrics
            .ConnectivityLoss
            .toFixed(4);

        document.getElementById(
            "resilience"
        ).innerText =

            data.resilience_score
            .toFixed(2) + "%";

        // ----------------------------------------
        // CRITICAL NODES
        // ----------------------------------------
        let criticalHTML = "";

        data.critical_nodes
        .forEach(node => {

            let utilization = (

                node.load /
                node.capacity *
                100

            ).toFixed(1);

            criticalHTML += `

                <div class="item">

                    <b>Node ${node.id}</b><br>

                    Utilization:
                    ${utilization}%

                </div>
            `;
        });

        document.getElementById(
            "critical"
        ).innerHTML = criticalHTML;

        // ----------------------------------------
        // RESET RECOVERY PANELS
        // ----------------------------------------
        document.getElementById(
            "strategy"
        ).innerHTML = `

            <div class="item">
                Select a recovery strategy.
            </div>
        `;

        document.getElementById(
            "timeline"
        ).innerHTML = `

            <div class="item">
                Recovery evolution
                will appear here.
            </div>
        `;
    });
}


// ----------------------------------------------------
// RECOVERY SIMULATION
// ----------------------------------------------------
function showRecovery(strategy) {

    let backendType = "random";

    // ----------------------------------------
    // STRATEGY TYPE
    // ----------------------------------------
    if (
        strategy ===
        "Load-Based Recovery"
    ) {

        backendType = "load";
    }

    else if (
        strategy ===
        "Centrality Recovery"
    ) {

        backendType = "centrality";
    }

    // ----------------------------------------
    // API CALL
    // ----------------------------------------
    fetch('/recover', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({

            recovery_type:
                backendType
        })
    })

    .then(res => res.json())

    .then(data => {

        // ----------------------------------------
        // NO RECOVERY DATA
        // ----------------------------------------
        if (
            !data.timeline ||
            data.timeline.length === 0
        ) {

            document.getElementById(
                "strategy"
            ).innerHTML = `

                <div class="item">

                    Run failure simulation first.

                </div>
            `;

            return;
        }

        // ----------------------------------------
        // FINAL STEP
        // ----------------------------------------
        let finalStep =

            data.timeline[
                data.timeline.length - 1
            ];

        // ----------------------------------------
        // VISUAL VALUES
        // ----------------------------------------
        let resiliencePercent =

            Math.min(
                100,
                finalStep.resilience
            );

        let efficiencyPercent =

            Math.min(
                100,
                finalStep.efficiency * 100
            );

        let connectivityPercent =

            Math.min(

                100,

                (
                    1 -
                    finalStep.connectivity_loss
                ) * 100
            );

        // ----------------------------------------
        // STRATEGY VISUAL CARD
        // ----------------------------------------
        document.getElementById(
            "strategy"
        ).innerHTML = `

            <div class="strategy-card">

                <div class="strategy-title">
                    ${strategy}
                </div>

                <!-- RESILIENCE -->
                <div class="metric-row">

                    <div class="metric-label">
                        Resilience Score
                    </div>

                    <div class="metric-bar">

                        <div class="metric-fill"

                             style="
                                width:
                                ${resiliencePercent}%;
                             ">
                        </div>

                    </div>

                    <div class="metric-text">

                        ${finalStep.resilience.toFixed(2)}%

                    </div>

                </div>


                <!-- EFFICIENCY -->
                <div class="metric-row">

                    <div class="metric-label">
                        Network Efficiency
                    </div>

                    <div class="metric-bar">

                        <div class="metric-fill"

                             style="
                                width:
                                ${efficiencyPercent}%;
                             ">
                        </div>

                    </div>

                    <div class="metric-text">

                        ${finalStep.efficiency.toFixed(4)}

                    </div>

                </div>


                <!-- CONNECTIVITY -->
                <div class="metric-row">

                    <div class="metric-label">
                        Connectivity Health
                    </div>

                    <div class="metric-bar">

                        <div class="metric-fill"

                             style="
                                width:
                                ${connectivityPercent}%;
                             ">
                        </div>

                    </div>

                    <div class="metric-text">

                        ${(1 -
                            finalStep.connectivity_loss
                        ).toFixed(4)}

                    </div>

                </div>


                <!-- STEPS -->
                <div class="metric-text">

                    Recovery Steps:
                    ${data.timeline.length}

                </div>

            </div>
        `;

        // ----------------------------------------
        // TIMELINE
        // ----------------------------------------
        let timelineHTML = "";

        data.timeline.forEach(step => {

            timelineHTML += `

                <div class="timeline-step">

                    <b>
                        Step ${step.step}
                    </b>

                    <br><br>

                    Resilience:
                    ${step.resilience.toFixed(2)}%
                    <br>

                    Efficiency:
                    ${step.efficiency.toFixed(4)}
                    <br>

                    Connectivity Loss:
                    ${step.connectivity_loss.toFixed(4)}

                </div>
            `;
        });

        document.getElementById(
            "timeline"
        ).innerHTML = timelineHTML;
    });
}


// ----------------------------------------------------
// RESET
// ----------------------------------------------------
function resetSimulation() {

    runSimulation("none");
}


// ----------------------------------------------------
// INITIAL LOAD
// ----------------------------------------------------
window.onload = () => {

    runSimulation("none");
};