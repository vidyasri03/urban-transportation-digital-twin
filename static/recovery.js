let recoveryMap = L.map(
    'recoveryMap'
).setView(
    [17.0, 81.8],
    13
);


// ========================================
// TILE LAYER
// ========================================
L.tileLayer(

    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

    {
        maxZoom: 19
    }

).addTo(recoveryMap);


let recoveryMarkers = [];


// ========================================
// NODE COLOR
// ========================================
function getRecoveryColor(node) {

    // failed
    if (node.status === "failed")
        return "#ff3b30";

    // recovering
    if (node.status === "recovering")
        return "#ffd60a";

    // congested
    if (node.status === "congested")
        return "#ff9500";

    // active
    return "#157d47";
}


// ========================================
// DRAW NETWORK
// ========================================
function drawRecoveryNodes(nodes) {

    recoveryMarkers.forEach(

        marker =>
            recoveryMap.removeLayer(marker)
    );

    recoveryMarkers = [];

    nodes.forEach(node => {

        let marker = L.circleMarker(

            [node.lat, node.lon],

            {
                radius: 6,

                color:
                    getRecoveryColor(node),

                fillColor:
                    getRecoveryColor(node),

                fillOpacity: 0.9,

                weight: 0
            }

        ).addTo(recoveryMap);

        marker.bindPopup(`

            <b>Node ${node.id}</b><br>

            Status:
            ${node.status}<br>

            Load:
            ${node.load.toFixed(2)}
            /
            ${node.capacity.toFixed(2)}

        `);

        recoveryMarkers.push(marker);
    });
}


// ========================================
// LOAD CURRENT NETWORK
// ========================================
function loadCurrentNetworkState() {

    fetch('/network_state')

    .then(res => res.json())

    .then(data => {

        if (
            data.nodes &&
            data.nodes.length > 0
        ) {

            drawRecoveryNodes(
                data.nodes
            );
        }
    });
}


// ========================================
// START RECOVERY
// ========================================
function startRecovery(strategy) {

    let backendType = "random";

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

    // ------------------------------------
    // CURRENT STRATEGY
    // ------------------------------------
    document.getElementById(
        "strategyPanel"
    ).innerHTML = `

        <div class="strategy-card">

            <div class="strategy-title">

                ${strategy}

            </div>

            Recovery simulation running...

        </div>
    `;

    // ------------------------------------
    // RUN RECOVERY
    // ------------------------------------
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

        if (
            !data.timeline ||
            data.timeline.length === 0
        ) {

            document.getElementById(
                "strategyPanel"
            ).innerHTML = `

                <div class="item">

                    Run failure simulation first.

                </div>
            `;

            return;
        }

        animateRecovery(
            data.timeline,
            strategy
        );
    });
}


// ========================================
// RECOVERY ANIMATION
// ========================================
function animateRecovery(

    timeline,

    strategy
) {

    let index = 0;

    let interval = setInterval(() => {

        if (
            index >= timeline.length
        ) {

            clearInterval(interval);

            return;
        }

        let step = timeline[index];

        // --------------------------------
        // DRAW NODES
        // --------------------------------
        if (step.nodes) {

            drawRecoveryNodes(
                step.nodes
            );
        }

        // --------------------------------
        // STRATEGY PANEL
        // --------------------------------
        document.getElementById(
            "strategyPanel"
        ).innerHTML = `

            <div class="strategy-card">

                <div class="strategy-title">

                    ${strategy}

                </div>

                <div class="metric-row">

                    <div class="metric-label">

                        Current Step

                    </div>

                    <div class="metric-text">

                        ${step.step}

                    </div>

                </div>

                <div class="metric-row">

                    <div class="metric-label">

                        Remaining Failed Nodes

                    </div>

                    <div class="metric-text">

                        ${step.remaining_failed}

                    </div>

                </div>

            </div>
        `;

        // --------------------------------
        // METRICS PANEL
        // --------------------------------
        document.getElementById(
            "recoveryMetrics"
        ).innerHTML = `

            <div class="strategy-card">

                <div class="metric-row">

                    <div class="metric-label">
                        Resilience
                    </div>

                    <div class="metric-text">
                        ${step.resilience.toFixed(2)}%
                    </div>

                </div>

                <div class="metric-row">

                    <div class="metric-label">
                        Efficiency
                    </div>

                    <div class="metric-text">
                        ${step.efficiency.toFixed(4)}
                    </div>

                </div>

                <div class="metric-row">

                    <div class="metric-label">
                        Connectivity Loss
                    </div>

                    <div class="metric-text">
                        ${step.connectivity_loss.toFixed(4)}
                    </div>

                </div>

            </div>
        `;

        // --------------------------------
        // TIMELINE
        // --------------------------------
        let timelineHTML = "";

        for (
            let i = 0;
            i <= index;
            i++
        ) {

            let t = timeline[i];

            timelineHTML += `

                <div class="timeline-step">

                    <b>
                        Step ${t.step}
                    </b>

                    <br><br>

                    Remaining Failed:
                    ${t.remaining_failed}
                    <br>

                    Resilience:
                    ${t.resilience.toFixed(2)}%
                    <br>

                    Efficiency:
                    ${t.efficiency.toFixed(4)}
                    <br>

                    Connectivity Loss:
                    ${t.connectivity_loss.toFixed(4)}

                </div>
            `;
        }

        document.getElementById(
            "timelinePanel"
        ).innerHTML = timelineHTML;

        index++;

    }, 800);
}


// ========================================
// COMPARE STRATEGIES
// ========================================
function compareStrategies() {

    fetch('/compare_recovery')

    .then(res => res.json())

    .then(data => {

        // --------------------------------
        // NO DATA
        // --------------------------------
        if (
            !data.strategies ||
            data.strategies.length === 0
        ) {

            document.getElementById(
                "comparisonPanel"
            ).innerHTML = `

                <div class="item">

                    Run recovery strategies first.

                </div>
            `;

            return;
        }

        // --------------------------------
        // BUILD TABLE
        // --------------------------------
        let html = "";

        data.strategies.forEach(strategy => {

            let bestBadge = "";

            if (
                strategy.strategy ===
                data.best_strategy
            ) {

                bestBadge = `
                    <div style="
                        color:#00ff88;
                        font-weight:bold;
                        margin-top:6px;
                    ">
                        BEST STRATEGY
                    </div>
                `;
            }

            html += `

                <div class="strategy-card">

                    <div class="strategy-title">

                        ${strategy.strategy}

                    </div>

                    Avg Resilience:
                    ${strategy.avg_resilience}%
                    <br><br>

                    Avg Connectivity:
                    ${strategy.avg_connectivity}%
                    <br><br>

                    Recovery Steps:
                    ${strategy.recovery_steps}
                    <br><br>

                    Final Resilience:
                    ${strategy.final_resilience}%
                    <br><br>

                    Performance Score:
                    ${strategy.score}

                    ${bestBadge}

                </div>
            `;
        });

        // --------------------------------
        // BEST STRATEGY
        // --------------------------------
        html += `

            <div class="strategy-card">

                <div class="strategy-title">

                    Recommended Strategy

                </div>

                <div style="
                    font-size:22px;
                    color:#00ff88;
                    font-weight:bold;
                    margin-bottom:12px;
                ">

                    ${data.best_strategy}

                </div>

                ${data.reason}

            </div>
        `;

        document.getElementById(
            "comparisonPanel"
        ).innerHTML = html;
    });
}


// ========================================
// INITIAL LOAD
// ========================================
window.onload = () => {

    loadCurrentNetworkState();
};