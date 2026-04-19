import { useState, useEffect } from "react";
import axios from "axios";

interface CarOptions {
  companies: string[];
  company_model_map: { [key: string]: string[] }; // This maps company name to list of models
  years: number[];
  fuel_types: string[];
}

function App() {
  const [options, setOptions] = useState<CarOptions | null>(null);
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
    // Debugging: See exactly what we are sending
    console.log("Sending to Backend:", formData);

    try {
      const res = await axios.post(
        "http://localhost:8080/api/cars/predict",
        formData,
      );
      setPrediction(res.data.price);
    } catch (err) {
      console.error("Prediction error:", err);
      alert("Error: Please make sure all fields are filled!");
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
              setFormData({ ...formData, company: e.target.value })
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
            disabled={!formData.company} // Disables dropdown until a company is selected
          >
            <option value="">
              {formData.company ? "Select Model" : "Select Company First"}
            </option>

            {/* Only show models if a company is selected */}
            {formData.company &&
              options?.company_model_map[formData.company] &&
              options.company_model_map[formData.company].map((m) => (
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

          <button type="submit">Predict Price</button>
        </form>
      ) : (
        <p>Loading options...</p>
      )}

      {prediction && <h2>Estimated Price: ₹{prediction}</h2>}
    </div>
  );
}

export default App;
