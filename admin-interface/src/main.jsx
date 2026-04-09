import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import { fetchOrders, fetchUsers, fetchTrackItems, fetchTrackFoodItems } from './api';


function App() {
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);
  const [trackItems, setTrackItems] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [foodStats, setFoodStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [foodLoading, setFoodLoading] = useState(false);
  const [foodError, setFoodError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [ordersData, usersData, trackItemsData] = await Promise.all([
          fetchOrders(),
          fetchUsers(),
          fetchTrackItems(),
        ]);
        setOrders(ordersData);
        setUsers(usersData);
        setTrackItems(trackItemsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  // Fetch food stats when a restaurant is selected
  useEffect(() => {
    if (!selectedRestaurant) return;
    setFoodLoading(true);
    setFoodError(null);
    fetchTrackFoodItems(selectedRestaurant.restaurant_id)
      .then(setFoodStats)
      .catch(err => setFoodError(err.message))
      .finally(() => setFoodLoading(false));
  }, [selectedRestaurant]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div style={{ padding: 24 }}>
      <h1>Admin Interface</h1>

      <h2>All Users</h2>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.email} ({user.first_name} {user.last_name}) - {user.role}</li>
        ))}
      </ul>

      <h2>All Orders</h2>
      <ul>
        {orders.map(order => (
          <li key={order.order_id}>Order #{order.order_id} - User: {order.customer_id} - Status: {order.status}</li>
        ))}
      </ul>


      <h2>Track Items (Restaurant Stats)</h2>
      <ul>
        {trackItems.map(stat => (
          <li key={stat.restaurant_id}>
            <button onClick={() => setSelectedRestaurant(stat)} style={{marginRight: 8}}>
              View Food Stats
            </button>
            Restaurant #{stat.restaurant_id} - {stat.restaurant_name} : {stat.order_count} orders
          </li>
        ))}
      </ul>

      {selectedRestaurant && (
        <div style={{marginTop: 24, border: '1px solid #ccc', padding: 16}}>
          <h3>Food Item Stats for {selectedRestaurant.restaurant_name}</h3>
          <button onClick={() => setSelectedRestaurant(null)} style={{marginBottom: 8}}>Close</button>
          {foodLoading && <div>Loading food stats...</div>}
          {foodError && <div style={{color: 'red'}}>Error: {foodError}</div>}
          {!foodLoading && !foodError && (
            <ul>
              {foodStats.length === 0 && <li>No food item stats found.</li>}
              {foodStats.map(item => (
                <li key={item.food_item_id}>
                  {item.food_item_name} - Ordered {item.order_count} times
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
