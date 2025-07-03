import React, { useState } from "react";

function App() {
  const [form, setForm] = useState({
    year: "",
    mileage: "",
    purchase_price: ""
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          year: Number(form.year),
          mileage: Number(form.mileage),
          purchase_price: Number(form.purchase_price),
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Something went wrong");
      } else {
        setResult(data);
      }
    } catch (err) {
      setError("Server error");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>AutoROI 🚗</h1>
      <form onSubmit={handleSubmit}>
        <input type="number" name="year" placeholder="Year" value={form.year} onChange={handleChange} /><br />
        <input type="number" name="mileage" placeholder="Mileage" value={form.mileage} onChange={handleChange} /><br />
        <input type="number" name="purchase_price" placeholder="Purchase Price" value={form.purchase_price} onChange={handleChange} /><br />
        <button type="submit">Calculate ROI</button>
      </form>

      {result && (
        <div>
          <h2>Results</h2>
          <p>Predicted Value: ${result.predicted_value}</p>
          <p>ROI: {result.roi_percent}%</p>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;