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

export async function fetchTrackItems() {
  const res = await fetch(`${BASE}/stat/restaurant/stats`);
  if (!res.ok) throw new Error("Failed to fetch track items");
  return res.json();
}

export async function fetchTrackFoodItems(restaurantId) {
  const res = await fetch(`${BASE}/food_stat/food_items/${restaurantId}/stats`);
  if (!res.ok) throw new Error("Failed to fetch track food items");
  return res.json();
}
