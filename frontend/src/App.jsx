import { useEffect, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000/api";

function App() {

  const [state,setState] = useState({});
  const [incidents,setIncidents] = useState([]);
  const [predictions,setPredictions] = useState([]);
  const [summary,setSummary] = useState("");
  const [zone,setZone] = useState({});
  const [plan,setPlan] = useState([]);
  const [demoResult,setDemoResult] = useState(null);

  async function fetchAPI(endpoint, setter){

    try{
      const res = await fetch(API + endpoint);
      const data = await res.json();
      setter(data);
    }
    catch(err){
      setter({error:err.message});
    }

  }


  useEffect(()=>{

    fetchAPI("/state",setState);
    fetchAPI("/incidents",setIncidents);
    fetchAPI("/predictions",setPredictions);
    fetchPlan();

    const timer=setInterval(()=>{
      fetchAPI("/state",setState);
      fetchAPI("/incidents",setIncidents);
    },5000);

    return ()=>clearInterval(timer);

  },[]);


  async function generateSummary(){

    const res=await fetch(API+"/summary");
    const data=await res.json();

    setSummary(
      data.summary || JSON.stringify(data)
    );

  }


  async function analyzeZone(){

    const res=await fetch(API+"/zones/Z1/analysis");
    const data=await res.json();

    setZone(data);

  }


  async function fetchPlan(){
    try{
      const res = await fetch(API+"/plan");
      const data = await res.json();
      setPlan(data.actions || []);
    }catch(e){
      setPlan([{error: e.message}]);
    }
  }


  async function executeAction(action){
    await fetch(API+"/actions/execute",{
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(action)
    });
    // refresh
    fetchPlan();
    fetchAPI('/incidents', setIncidents);
  }


  async function runDemo(){
    try{
      const res = await fetch(API+"/demo/run",{method:'POST'});
      const data = await res.json();
      setDemoResult(data.timeline || []);
      // refresh state and plan
      fetchAPI('/state', setState);
      fetchPlan();
    }catch(e){
      setDemoResult([{error: e.message}]);
    }
  }


return (

<div className="app">

<header>
<h1>🏟 StadiumOS AI</h1>
<p>Generative AI Stadium Operations Platform</p>
<div className="live">● LIVE</div>
</header>


<section className="cards">

<div className="card">
<h3>Current Crowd</h3>
<h1>
{state.total_population || state.current_occupancy || "—"}
</h1>
</div>


<div className="card">
<h3>Active Incidents</h3>
<h1>{incidents.length}</h1>
</div>


<div className="card">
<h3>Predictions</h3>
<h1>{predictions.length}</h1>
</div>


<div className="card">
<h3>Status</h3>
<h1 className="green">ONLINE</h1>
</div>

</section>


<section className="grid">

<div className="panel">
  <h2>🧭 Live Planner</h2>
  <button onClick={fetchPlan}>Fetch Plan</button>
  <div className="plan-list">
    {plan.length===0 && <div className="muted">No actions recommended.</div>}
    {plan.map((a,i)=> (
      <div className="plan-item" key={i}>
        <div><strong>{a.priority || 'info'}</strong> — {a.message}</div>
        <div style={{marginTop:6}}>
          <button onClick={()=>executeAction(a)}>Execute</button>
        </div>
      </div>
    ))}
  </div>
  <div style={{marginTop:12}}>
    <button onClick={runDemo}>Run Automated Demo</button>
  </div>
  {demoResult && (
    <div style={{marginTop:12}}>
      <h4>Demo Timeline</h4>
      <pre style={{maxHeight:240, overflow:'auto'}}>{JSON.stringify(demoResult,null,2)}</pre>
    </div>
  )}
</div>


<div className="panel">
<h2>🚨 Incidents</h2>

{
incidents.map((x,i)=>
<div className="item" key={i}>
{JSON.stringify(x)}
</div>
)
}

</div>



<div className="panel">

<h2>🤖 AI Executive Summary</h2>

<button onClick={generateSummary}>
Generate
</button>

<p>
{summary || "Click generate"}
</p>

</div>



<div className="panel">

<h2>👥 Crowd Analysis</h2>

<button onClick={analyzeZone}>
Analyze Zone Z1
</button>

{zone && zone.error ? (
  <div className="error">Error: {zone.error}</div>
) : (
  <div className="zone-result">
    <div><strong>Zone:</strong> {zone.zone || 'Z1'}</div>
    <div><strong>Density:</strong> {zone.density ?? (zone.predicted_crowd_density ?? '—')}</div>
    <div><strong>Risk:</strong> {zone.congestion_risk ?? zone.congestion_probability ?? '—'}</div>
    <div><strong>Recommendation:</strong> {zone.recommendation || zone.reasoning || '—'}</div>
    {zone.incidents && zone.incidents.length > 0 && (
      <div><strong>Incidents:</strong> {zone.incidents.join(', ')}</div>
    )}
    {zone.source && <div className="muted">Source: {zone.source}</div>}
  </div>
)}


</div>


</section>


</div>

)

}

export default App;