import React, { useEffect, useState } from "react";
import './RestaurantStats.css';
import axios from "axios";

const RestaurantStats = () => {
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/stat/restaurant/stats");
        setStats(response.data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setError("Failed to load restaurant stats");
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) return <p>Loading stats...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2 style={{ backgroundColor: "lightyellow" }}>Restaurant Order Stats</h2>
      <div className="statsTable">
        <table className="statsT">
          <thead>
            <tr>
              <th>Restaurant ID</th>
              <th>Order Count</th>
            </tr>
          </thead>
          <tbody>
            {stats
              .filter(stat => typeof stat.restaurant_name === "string" && stat.restaurant_name.trim() !== "")
              .map((stat, index) => (
                <tr key={index}>
                  <td>{stat.restaurant_name}</td>
                  <td>{stat.order_count}</td>
                </tr>
              ))
            }
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RestaurantStats;