import React, { useState, useEffect } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion"; // Add these imports

interface CarOptions {
  companies: string[];
  company_model_map: { [key: string]: string[] };
  years: number[];
  fuel_types: string[];
}

function App() {
  const [options, setOptions] = useState<CarOptions | null>(null);
  const [loading, setLoading] = useState(false); // Loading state added

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
    setLoading(true); // Start loading
    setPrediction(null); // Clear old result

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
      setLoading(false); // Stop loading regardless of result
    }
  };

  return (
    <div style={{ padding: "50px", maxWidth: "600px", margin: "auto" }}>
      <h1>Car Price Predictor</h1>

      {options ? (
        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", flexDirection: "column", gap: "10px" }}
        >
          <select
            value={formData.company}
            onChange={(e) =>
              setFormData({ ...formData, company: e.target.value, name: "" })
            }
          >
            <option value="">Select Company</option>
            {options.companies.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>

          <select
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
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

          <select
            value={formData.year}
            onChange={(e) => setFormData({ ...formData, year: e.target.value })}
          >
            <option value="">Select Year</option>
            {options.years.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>

          <input
            type="number"
            placeholder="Kilometers Driven"
            value={formData.kms_driven}
            onChange={(e) =>
              setFormData({ ...formData, kms_driven: e.target.value })
            }
          />

          <select
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

          <button type="submit" disabled={loading}>
            {loading ? "Predicting..." : "Predict Price"}
          </button>

          {loading && <p style={{ color: "blue" }}>Processing your data...</p>}
        </form>
      ) : (
        <p>Loading options...</p>
      )}

      <AnimatePresence>
        {prediction && (
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            Estimated Price: ₹{prediction}
          </motion.h2>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
