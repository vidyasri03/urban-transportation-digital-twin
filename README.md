@'
# 🚦 Urban Transportation Digital Twin

## 📌 Project Overview

The **Urban Transportation Digital Twin** is a simulation and analysis platform designed to model urban transportation networks, simulate traffic conditions, identify critical infrastructure components, and evaluate network behavior under disruptions.

The system provides an interactive web-based dashboard where users can simulate transportation network failures, observe cascading effects, analyze network resilience, and compare different recovery strategies.

---

## 🎯 Objectives

- Model an urban transportation network as a digital twin.
- Simulate traffic loads and network disruptions.
- Identify critical and high-utilization infrastructure nodes.
- Analyze cascading failures across the transportation network.
- Measure network resilience, efficiency, and connectivity.
- Simulate and compare different recovery strategies.

---

## ✨ Key Features

- 🗺️ Interactive Transportation Network Map
- 🚗 Dynamic Traffic Load Simulation
- ⚠️ Random Failure Simulation
- 🎯 Targeted / Critical Node Failure
- 🔄 Cascading Failure Analysis
- 📊 Network Metrics and Resilience Analysis
- 🛠️ Recovery Strategy Simulation
- 📈 Recovery Strategy Comparison
- 🟢 Critical Infrastructure Identification
- 🌐 Flask-based Web Dashboard

---

## 🧠 System Workflow

```text
Urban Transportation Network
            ↓
     Network Initialization
            ↓
      Dynamic Load Assignment
            ↓
       Failure Simulation
            ↓
      Cascading Failures
            ↓
     Network Metrics Analysis
            ↓
      Recovery Simulation
            ↓
   Recovery Strategy Comparison
```
## 🔬 Simulation Scenarios

### 1. Initial State

Displays the transportation network before any disruption.

### 2. Random Failure

Randomly selects transportation nodes for failure and evaluates the effect on the network.

### 3. Targeted Attack

Targets important or highly critical nodes to study the effect of strategic infrastructure failures.

### 4. Cascading Failure

Simulates how an initial failure can overload neighboring nodes and cause additional failures throughout the transportation network.

### 5. Recovery Strategies

The system supports multiple recovery approaches:

- Random Recovery
- Load-Based Recovery
- Centrality-Based Recovery

These strategies are evaluated using network resilience, connectivity, efficiency, and recovery performance.

---

## 📊 Network Metrics

The dashboard provides metrics such as:

- Active Nodes
- Failed Nodes
- Network Efficiency
- Connectivity Loss
- Resilience Score
- Node Utilization
- Recovery Steps
- Strategy Performance Score

---

## 🛠️ Technologies Used

- Python
- Flask
- NetworkX
- OSMnx
- Pandas
- NumPy
- HTML
- CSS
- JavaScript
- Interactive Mapping
- Pytest

---

## 📂 Project Structure

```text
urban-transportation-digital-twin/
│
├── src/
│   ├── analysis/
│   ├── api/
│   ├── metrics/
│   ├── preprocessing/
│   ├── recovery/
│   └── simulation/
│
├── data/
│
├── static/
│   ├── css/
│   ├── main.js
│   ├── recovery.js
│   └── style.css
│
├── templates/
│   ├── analytics.html
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── map.html
│   └── recovery.html
│
├── Project-Screenshots/
│   ├── Dashboard.png
│   ├── Failure_Simulation.png
│   ├── Recovery_dashboard.png
│   └── Comparing_dashboard.png
│
├── app.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```
@'

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vidyasri03/urban-transportation-digital-twin.git
```
### 2. Navigate to the Project Directory
```bash
cd urban-transportation-digital-twin
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the application
```bash
python app.py
```
5. Open the Application

Open the application in your browser:

```bash
http://127.0.0.1:5000/
```
$readme = Get-Content README.md -Raw

$screenshots = @'
## 📸 Project Screenshots

### 🏠 Main Dashboard

<p align="center">
  <img src="./Project-Screenshots/Dashboard.png" alt="Urban Transportation Digital Twin - Main Dashboard" width="100%">
</p>

### ⚠️ Failure Simulation

<p align="center">
  <img src="./Project-Screenshots/Failure_Simulation.png" alt="Urban Transportation Digital Twin - Failure Simulation" width="100%">
</p>

### 🔄 Recovery Dashboard

<p align="center">
  <img src="./Project-Screenshots/Recovery_dashboard.png" alt="Urban Transportation Digital Twin - Recovery Dashboard" width="100%">
</p>

### 📊 Recovery Strategy Comparison

<p align="center">
  <img src="./Project-Screenshots/Comparing_dashboard.png" alt="Urban Transportation Digital Twin - Recovery Strategy Comparison" width="100%">
</p>

---

'@

$readme = [regex]::Replace(
    $readme,
    '(?s)## 📸 Project Screenshots.*?(?=## 🚀 Applications)',
    $screenshots
)

Set-Content README.md $readme -Encoding UTF8

git add README.md
git commit -m "Display project screenshots in README"
git push

$readme = Get-Content README.md -Raw

$replacement = @'
## 🚀 Applications

This project can be used for studying:

- Urban transportation resilience
- Infrastructure vulnerability
- Traffic disruption scenarios
- Cascading network failures
- Emergency recovery planning
- Transportation network optimization
- Digital twin based transportation analysis

---

## 🔮 Future Enhancements

- Real-time traffic data integration
- Larger and more detailed transportation networks
- Real-time digital twin synchronization
- Advanced predictive failure analysis
- Intelligent recovery optimization
- Cloud-based deployment
- Real-time visualization and monitoring

---

## 👩‍💻 Author

**Vidyasri**

---

