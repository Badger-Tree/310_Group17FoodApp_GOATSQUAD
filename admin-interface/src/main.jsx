import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import { fetchOrders, fetchUsers } from './api';

function App() {
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [ordersData, usersData] = await Promise.all([
          fetchOrders(),
          fetchUsers(),
        ]);
        setOrders(ordersData);
        setUsers(usersData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

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
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
