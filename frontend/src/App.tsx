import React, { useState, useEffect } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import "./App.css"; // Make sure this is imported!

interface CarOptions {
  companies: string[];
  company_model_map: { [key: string]: string[] };
  years: number[];
  fuel_types: string[];
}

function App() {
  const [options, setOptions] = useState<CarOptions | null>(null);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    company: "",
    name: "",
    year: "",
    kms_driven: "",
    fuel_type: "",
  });
  const [prediction, setPrediction] = useState<number | null>(null);

  useEffect(() => {
    axios
      .get("http://localhost:8080/api/cars/options")
      .then((res) => setOptions(res.data))
      .catch((err) => console.error("Error fetching options:", err));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);

    try {
      const res = await axios.post(
        "http://localhost:8080/api/cars/predict",
        formData,
      );
      setPrediction(res.data.price);
    } catch (err) {
      console.error("Prediction error:", err);
      alert("Error: Please make sure all fields are filled!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-card">
      {/* Header Section */}
      <div className="card-header">
        <h1>Predict Price</h1>
        <p>Enter vehicle details to estimate its market value.</p>
      </div>

      {/* Body Section */}
      <div className="card-body">
        {options ? (
          <form onSubmit={handleSubmit} className="form-layout">
            <div className="input-group">
              <label>Manufacturer</label>
              <select
                className="premium-input"
                value={formData.company}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    company: e.target.value,
                    name: "",
                  })
                }
              >
                <option value="">Select Company</option>
                {options.companies.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>

            <div className="input-group">
              <label>Vehicle Model</label>
              <select
                className="premium-input"
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                disabled={!formData.company}
              >
                <option value="">
                  {formData.company ? "Select Model" : "Select Company First"}
                </option>
                {formData.company &&
                  options?.company_model_map[formData.company]?.map((m) => (
                    <option key={m} value={m}>
                      {m}
                    </option>
                  ))}
              </select>
            </div>

            <div className="input-group">
              <label>Manufacturing Year</label>
              <select
                className="premium-input"
                value={formData.year}
                onChange={(e) =>
                  setFormData({ ...formData, year: e.target.value })
                }
              >
                <option value="">Select Year</option>
                {options.years.map((y) => (
                  <option key={y} value={y}>
                    {y}
                  </option>
                ))}
              </select>
            </div>

            <div className="input-group">
              <label>Kilometers Driven</label>
              <input
                className="premium-input"
                type="number"
                placeholder="e.g. 45000"
                value={formData.kms_driven}
                onChange={(e) =>
                  setFormData({ ...formData, kms_driven: e.target.value })
                }
              />
            </div>

            <div className="input-group">
              <label>Fuel Type</label>
              <select
                className="premium-input"
                value={formData.fuel_type}
                onChange={(e) =>
                  setFormData({ ...formData, fuel_type: e.target.value })
                }
              >
                <option value="">Select Fuel Type</option>
                {options.fuel_types.map((f) => (
                  <option key={f} value={f}>
                    {f}
                  </option>
                ))}
              </select>
            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? "Processing..." : "Calculate Price"}
            </button>
          </form>
        ) : (
          <p style={{ color: "#6c757d", textAlign: "center" }}>
            Connecting to data models...
          </p>
        )}

        {/* Framer Motion Animation for Result */}
        <AnimatePresence>
          {prediction && (
            <motion.h2
              className="result-display"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, ease: "easeOut" }}
            >
              ₹{prediction.toLocaleString("en-IN")}
            </motion.h2>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
