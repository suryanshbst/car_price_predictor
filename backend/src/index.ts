import express, { Request, Response } from "express";
import cors from "cors";
import axios from "axios";

const app = express();
const PORT = 8080;
const PYTHON_API_URL = "http://localhost:5000/api";

// Middleware
app.use(cors());
app.use(express.json());

// Strict TypeScript Interface for our incoming car data
interface CarData {
  name: string;
  company: string;
  year: number;
  kms_driven: number;
  fuel_type: string;
}

// 1. Endpoint to fetch dropdown options (Proxies to Python)
app.get("/api/cars/options", async (req: Request, res: Response) => {
  try {
    const response = await axios.get(`${PYTHON_API_URL}/options`);
    res.json(response.data);
  } catch (error) {
    console.error("Error fetching options:", error);
    res
      .status(500)
      .json({ message: "Failed to fetch options from ML service" });
  }
});

// 2. Endpoint to predict price (Proxies to Python)
app.post(
  "/api/cars/predict",
  async (req: Request<{}, {}, CarData>, res: Response) => {
    try {
      // req.body is strictly typed as CarData
      const carData = req.body;

      // Forward the validated data to the Python microservice
      const response = await axios.post(`${PYTHON_API_URL}/predict`, carData);
      res.json(response.data);
    } catch (error) {
      console.error("Prediction error:", error);
      res.status(500).json({ message: "Prediction failed" });
    }
  },
);

app.listen(PORT, () => {
  console.log(`🚀 Node.js Backend running on http://localhost:${PORT}`);
});
