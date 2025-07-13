import React, { useState, useMemo, useEffect } from 'react';
import msrpData from './msrp_data.json'; 
import logo from './logo.png'; 


const brandModelYearMap = (() => {
  const map = {};
  Object.keys(msrpData).forEach((key) => {
    const parts = key.split('_');
    const year = parts.pop();
    const brand = parts.shift();
    const model = parts.join('_');
    if (!map[brand]) map[brand] = {};
    if (!map[brand][model]) map[brand][model] = new Set();
    map[brand][model].add(year);
  });
  Object.keys(map).forEach((brand) => {
    Object.keys(map[brand]).forEach((model) => {
      map[brand][model] = Array.from(map[brand][model]).sort((a, b) => b - a);
    });
  });
  return map;
})();

function App() {
  const [form, setForm] = useState({
    brand: '',
    model: '',
    year: '',
    mileage: '',
    drivetrain: '',
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
      // reset dependent fields
      ...(name === 'brand' && { model: '', year: '' }),
      ...(name === 'model' && { year: '' }),
    }));
  };

  const estimateMsrp = (brand, model, year) => {
    const exactKey = `${brand}_${model}_${year}`;
    if (msrpData[exactKey]) return msrpData[exactKey];
    const modelKeys = Object.keys(msrpData).filter(k => k.startsWith(`${brand}_${model}_`));
    if (modelKeys.length) {
      return Math.round(modelKeys.reduce((sum, k) => sum + msrpData[k], 0) / modelKeys.length);
    }
    const brandKeys = Object.keys(msrpData).filter(k => k.startsWith(`${brand}_`));
    if (brandKeys.length) {
      return Math.round(brandKeys.reduce((sum, k) => sum + msrpData[k], 0) / brandKeys.length);
    }
    return 30000;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    const msrp = estimateMsrp(form.brand, form.model, form.year);

    try {
      const res = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          brand: form.brand,
          model: form.model,
          year: Number(form.year),
          mileage: Number(form.mileage),
          drivetrain: form.drivetrain,
          msrp,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || 'Unexpected error');
      } else {
        setResult(data.predicted_value);
      }
    } catch {
      setError('Server error');
    }
  };

  
  const handleClear = () => {
    setForm({ brand: '', model: '', year: '', mileage: '', drivetrain: '' });
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[length:200%_200%] bg-gradient-to-r from-black via-red-900 to-red-500 animate-gradient-x">
      <header className="bg-gradient-to-r from-black to-red-700 shadow">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-start pl-6">
          <img src={logo} alt="AutoVise Logo" className="h-20 w-auto" />
        </div>
      </header>

      <main className="flex-grow flex items-center justify-center px-4 py-8">
        <div className="relative">
          <div className="w-full max-w-lg bg-white bg-opacity-90 backdrop-blur-lg p-8 rounded-xl shadow-xl border-2 border-red-200 relative z-10">
          <h2 className="text-2xl font-bold mb-6 bg-clip-text text-transparent bg-[length:200%_200%] bg-gradient-to-r from-black via-red-900 to-red-500 animate-gradient-x">
            Enter Specs Here
          </h2>
          <form onSubmit={handleSubmit} className="space-y-5">
            <input
              list="brand-list"
              name="brand"
              value={form.brand}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400"
              placeholder="Select or Type Brand"
            />
            <datalist id="brand-list">
              {Object.keys(brandModelYearMap).map((b) => (
                <option key={b} value={b} />
              ))}
            </datalist>
            <input
              list="model-list"
              name="model"
              value={form.model}
              onChange={handleChange}
              disabled={!form.brand}
              className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 disabled:opacity-50"
              placeholder="Select or Type Model"
            />
            <datalist id="model-list">
              {form.brand && brandModelYearMap[form.brand] &&
                Object.keys(brandModelYearMap[form.brand]).map((m) => (
                  <option key={m} value={m} />
                ))}
            </datalist>
            <input
              list="year-list"
              name="year"
              value={form.year}
              onChange={handleChange}
              disabled={!form.model}
              className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 disabled:opacity-50"
              placeholder="Select or Type Year"
            />
            <datalist id="year-list">
              {form.brand && form.model && brandModelYearMap[form.brand] &&
                brandModelYearMap[form.brand][form.model] &&
                brandModelYearMap[form.brand][form.model].map((y) => (
                  <option key={y} value={y} />
                ))}
            </datalist>
            <input
              type="number"
              name="mileage"
              placeholder="Mileage"
              value={form.mileage}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
            <input
              type="text"
              name="drivetrain"
              placeholder="Drivetrain (e.g. FWD, AWD)"
              value={form.drivetrain}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-black to-red-600 text-white py-3 rounded-lg font-medium hover:from-black hover:to-red-700 transition"
            >
              Estimate Value
            </button>
            <button
              type="button"
              onClick={handleClear}
              className="w-full bg-[length:200%_200%] bg-gradient-to-r from-black via-red-900 to-red-500 animate-gradient-x text-white py-3 rounded-lg font-medium hover:from-black hover:to-red-700 transition mt-2"
            >
              Clear
            </button>
          </form>


          {result !== null && (
            <div className="mt-8 p-4 bg-gradient-to-r from-red-200 to-red-100 border border-red-300 rounded-lg shadow-md">
              <h3 className="text-lg font-medium text-green-700">Estimated Value</h3>
              <p className="mt-2 text-2xl font-bold text-green-800">${result.toLocaleString()}</p>
            </div>
          )}
          {error && (
            <p className="mt-6 text-red-600 text-center">{error}</p>
          )}
          </div>
        </div>
      </main>


      <footer className="bg-gradient-to-r from-black to-red-100 shadow-inner">
        <div className="max-w-7xl mx-auto px-6 py-4 text-center text-red-700 text-sm">
          © 2025 AutoROI. All rights reserved.
        </div>
      </footer>
    </div>
  );
}

export default App;
