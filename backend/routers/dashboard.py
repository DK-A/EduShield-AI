from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from urllib.parse import unquote
from database.db import SessionLocal
from database.models import EmailScan

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# =========================================
# DASHBOARD PAGE
# =========================================
@router.get("/{email}", response_class=HTMLResponse)
def dashboard_page(email: str):

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>EduShield SOC</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body {{
    margin:0;
    padding:30px;
    background:#0f172a;
    font-family:Segoe UI;
    color:#e2e8f0;
}}

.container {{
    max-width:1200px;
    margin:auto;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:20px;
}}

.card {{
    background:#1e293b;
    padding:20px;
    border-radius:12px;
}}

.metric {{
    font-size:26px;
    font-weight:600;
}}

.high {{ color:#ef4444; }}
.medium {{ color:#facc15; }}
.low {{ color:#22c55e; }}

table {{
    width:100%;
    margin-top:20px;
    border-collapse:collapse;
}}

th,td {{
    padding:10px;
    border-bottom:1px solid #334155;
}}

th {{ opacity:0.6; }}

.modal {{
    position:fixed;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    background:#1e293b;
    padding:20px;
    border-radius:10px;
    display:none;
}}

.modal-close {{
    cursor:pointer;
    float:right;
    color:#ef4444;
}}
</style>
</head>

<body>
<div class="container">

<h2>EduShield Security Dashboard</h2>

<div class="grid">
<div class="card">
<div>Security Score</div>
<div id="score" class="metric">--</div>
</div>

<div class="card">
<div>High Risk</div>
<div id="high" class="metric high">--</div>
</div>

<div class="card">
<div>Medium Risk</div>
<div id="medium" class="metric medium">--</div>
</div>

<div class="card">
<div>Low Risk</div>
<div id="low" class="metric low">--</div>
</div>
</div>

<div class="card" style="margin-top:20px;">
<canvas id="trendChart"></canvas>
</div>

<div class="card" style="margin-top:20px;">
<table>
<thead>
<tr>
<th>Subject</th>
<th>Risk</th>
<th>Score</th>
</tr>
</thead>
<tbody id="emailTable"></tbody>
</table>
</div>

</div>

<div id="modal" class="modal">
<span class="modal-close" onclick="closeModal()">✖</span>
<h3>AI Explanation</h3>
<div id="modalContent"></div>
</div>

<script>

const email = "{email}";

function closeModal(){{
    document.getElementById("modal").style.display="none";
}}

function showExplanation(element){{
    const exp = JSON.parse(element.getAttribute("data-exp"));
    let html="";
    exp.forEach(e=> html += "• "+e+"<br>");
    document.getElementById("modalContent").innerHTML = html;
    document.getElementById("modal").style.display="block";
}}

const trendChart = new Chart(
    document.getElementById("trendChart"),
    {{
        type:"line",
        data:{{ labels:[], datasets:[{{ data:[], borderColor:"#38bdf8" }}] }},
        options:{{ plugins:{{ legend:{{display:false}} }} }}
    }}
);

function loadDashboard(){{
    fetch("/dashboard/data/" + email)
    .then(res=>res.json())
    .then(data=>{{

        document.getElementById("score").innerText = data.security_score;
        document.getElementById("high").innerText = data.high;
        document.getElementById("medium").innerText = data.medium;
        document.getElementById("low").innerText = data.low;

        trendChart.data.labels = data.trend_labels;
        trendChart.data.datasets[0].data = data.trend_values;
        trendChart.update();

        const table = document.getElementById("emailTable");
        table.innerHTML="";

        data.emails.forEach(e=>{{
            let explanation = JSON.stringify(e.explanation).replace(/'/g,"&apos;");

            table.innerHTML += `
            <tr>
            <td style="cursor:pointer;color:#38bdf8;"
                data-exp='${{explanation}}'
                onclick="showExplanation(this)">
                ${{
                    e.subject
                }}
            </td>
            <td class="${{e.risk_level.toLowerCase()}}">
                ${{
                    e.risk_level
                }}
            </td>
            <td>${{
                e.risk_score
            }}</td>
            </tr>
            `;
        }});
    }});
}}

loadDashboard();
setInterval(loadDashboard,10000);

</script>

</body>
</html>
"""


# =========================================
# DATA API
# =========================================
@router.get("/data/{email}")
def dashboard_data(email: str):

    email = unquote(email)
    db: Session = SessionLocal()

    scans = db.query(EmailScan).filter(
        EmailScan.user_email == email
    ).order_by(
        EmailScan.created_at.desc()
    ).limit(5).all()

    if not scans:
        db.close()
        return {
            "security_score":100,
            "high":0,
            "medium":0,
            "low":0,
            "trend_labels":[],
            "trend_values":[],
            "emails":[]
        }

    high = sum(1 for s in scans if s.risk_level=="High")
    medium = sum(1 for s in scans if s.risk_level=="Medium")
    low = sum(1 for s in scans if s.risk_level=="Low")

    # SECURITY SCORE = AVERAGE SAFETY SCORE
    avg_score = sum(s.risk_score for s in scans) / len(scans)
    security_score = int(avg_score)

    trend_labels = [s.created_at.strftime("%H:%M") for s in scans]
    trend_values = [int(s.risk_score) for s in scans]

    def generate_explanation(level):
        if level=="High":
            return [
                "Email shows strong phishing indicators",
                "Low trust score from model",
                "Recommended: Do not click links"
            ]
        elif level=="Medium":
            return [
                "Moderate suspicious signals detected",
                "Contains external references",
                "Proceed with caution"
            ]
        else:
            return [
                "High safety score",
                "Trusted communication pattern",
                "No phishing signals detected"
            ]

    emails = [{
        "subject": s.subject,
        "risk_level": s.risk_level,
        "risk_score": s.risk_score,
        "explanation": generate_explanation(s.risk_level)
    } for s in scans]

    db.close()

    return {
        "security_score":security_score,
        "high":high,
        "medium":medium,
        "low":low,
        "trend_labels":trend_labels[::-1],
        "trend_values":trend_values[::-1],
        "emails":emails
    }