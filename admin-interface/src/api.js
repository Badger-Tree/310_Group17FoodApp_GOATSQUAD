// Utility to fetch from backend (adjust URL if needed)
const BASE = "http://localhost:8000";

export async function fetchOrders() {
  const res = await fetch(`${BASE}/orders/orders`);
  if (!res.ok) throw new Error("Failed to fetch orders");
  return res.json();
}

export async function fetchUsers() {
  const res = await fetch(`${BASE}/users/users`);
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
}
