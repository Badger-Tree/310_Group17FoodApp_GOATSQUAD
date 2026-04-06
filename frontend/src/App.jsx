import { useEffect, useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
const AUTH_STORAGE_KEY = 'goat-food-auth';

function formatMoney(value) {
  const number = Number(value);
  return Number.isNaN(number) ? '-' : number.toFixed(2);
}

function App() {
  const [restaurants, setRestaurants] = useState([]);
  const [foodItems, setFoodItems] = useState([]);
  const [cart, setCart] = useState(null);
  const [cartQuantities, setCartQuantities] = useState({});
  const [loadingRestaurants, setLoadingRestaurants] = useState(true);
  const [loadingFood, setLoadingFood] = useState(true);
  const [loadingCart, setLoadingCart] = useState(false);
  const [restaurantError, setRestaurantError] = useState('');
  const [foodError, setFoodError] = useState('');
  const [cartError, setCartError] = useState('');
  const [authError, setAuthError] = useState('');
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [auth, setAuth] = useState(() => {
    if (typeof window === 'undefined') {
      return null;
    }
    const saved = localStorage.getItem(AUTH_STORAGE_KEY);
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    const loadRestaurants = async () => {
      setLoadingRestaurants(true);
      setRestaurantError('');

      try {
        const response = await fetch(`${API_BASE_URL}/restaurants/sort/name`);
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        const data = await response.json();
        setRestaurants(Array.isArray(data) ? data : []);
      } catch (err) {
        setRestaurantError(`Unable to load restaurants. ${err.message}`);
      } finally {
        setLoadingRestaurants(false);
      }
    };

    const loadFoodItems = async () => {
      setLoadingFood(true);
      setFoodError('');

      try {
        const response = await fetch(`${API_BASE_URL}/food-items`);
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        const data = await response.json();
        const items = Array.isArray(data) ? data : [];
        setFoodItems(items);
        const initialQuantities = items.reduce((acc, item) => {
          const id = item.food_item_id ?? item.id;
          if (id != null) {
            acc[id] = 1;
          }
          return acc;
        }, {});
        setCartQuantities(initialQuantities);
      } catch (err) {
        setFoodError(`Unable to load food items. ${err.message}`);
      } finally {
        setLoadingFood(false);
      }
    };

    loadRestaurants();
    loadFoodItems();
  }, []);

  useEffect(() => {
    if (!auth) {
      localStorage.removeItem(AUTH_STORAGE_KEY);
      setCart(null);
      return;
    }

    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(auth));
    if (auth.user_id) {
      loadCart(auth.user_id);
    }
  }, [auth]);

  const authHeaders = () => ({
    token: auth?.token || '',
    'Content-Type': 'application/json',
  });

  const loadCart = async (customerId) => {
    if (!customerId) return;
    setLoadingCart(true);
    setCartError('');

    try {
      const response = await fetch(`${API_BASE_URL}/cart/get?customer_id=${encodeURIComponent(customerId)}`);
      if (response.status === 404) {
        setCart({ customer_id: customerId, cart_id: '', cart_items: [], total: 0 });
        return;
      }
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      const data = await response.json();
      setCart(data);
    } catch (err) {
      setCartError(`Unable to load cart. ${err.message}`);
    } finally {
      setLoadingCart(false);
    }
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    setAuthError('');

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: loginEmail, password: loginPassword }),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Login failed (${response.status}) ${body}`);
      }
      const data = await response.json();
      setAuth(data);
      setLoginEmail('');
      setLoginPassword('');
    } catch (err) {
      setAuthError(err.message);
    }
  };

  const handleLogout = async () => {
    setAuthError('');
    try {
      if (!auth?.token) {
        setAuth(null);
        return;
      }
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: { token: auth.token },
      });
    } catch (err) {
      console.warn(err);
    } finally {
      setAuth(null);
    }
  };

  const handleQuantityChange = (foodId, value) => {
    setCartQuantities((prev) => ({
      ...prev,
      [foodId]: Math.max(1, Number(value) || 1),
    }));
  };

  const handleAddToCart = async (foodItemId) => {
    if (!auth?.token) {
      setCartError('You must login before adding items to the cart.');
      return;
    }
    setCartError('');
    try {
      const response = await fetch(`${API_BASE_URL}/cart/food_item/add`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({
          food_item_id: foodItemId,
          quantity: cartQuantities[foodItemId] || 1,
        }),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Failed to add item (${response.status}) ${body}`);
      }
      const updatedCart = await response.json();
      setCart(updatedCart);
    } catch (err) {
      setCartError(err.message);
    }
  };

  const handleRemoveCartItem = async (cartItemId) => {
    if (!auth?.token) {
      setCartError('You must login before modifying your cart.');
      return;
    }
    setCartError('');
    try {
      const response = await fetch(`${API_BASE_URL}/cart/food_item/remove?cart_item_id=${encodeURIComponent(cartItemId)}`, {
        method: 'DELETE',
        headers: { token: auth.token },
      });
      if (!response.ok) {
        throw new Error(`Failed to remove item (${response.status})`);
      }
      await loadCart(auth.user_id);
    } catch (err) {
      setCartError(err.message);
    }
  };

  const handleUpdateCartItem = async (cartItem) => {
    if (!auth?.token) {
      setCartError('You must login before modifying your cart.');
      return;
    }
    setCartError('');
    try {
      const response = await fetch(`${API_BASE_URL}/cart/food_item/update?cart_item_id=${encodeURIComponent(cartItem.cart_item_id)}`, {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify({
          food_item_id: cartItem.food_item_id,
          quantity: cartItem.quantity,
        }),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Failed to update item (${response.status}) ${body}`);
      }
      await loadCart(auth.user_id);
    } catch (err) {
      setCartError(err.message);
    }
  };

  const renderCartItems = () => {
    if (!cart?.cart_items || cart.cart_items.length === 0) {
      return <p>Your cart is empty.</p>;
    }
    return (
      <div className="cart-list">
        {cart.cart_items.map((item) => (
          <article key={item.cart_item_id} className="cart-item-card">
            <div>
              <p><strong>Food item:</strong> {item.food_item_id}</p>
              <p><strong>Price:</strong> ${formatMoney(item.price_per_item)}</p>
              <p><strong>Subtotal:</strong> ${formatMoney(item.subtotal)}</p>
            </div>
            <div className="cart-actions">
              <label>
                Quantity
                <input
                  type="number"
                  min="1"
                  value={item.quantity}
                  onChange={(event) => {
                    const value = Math.max(1, Number(event.target.value) || 1);
                    setCart((prev) => {
                      if (!prev) return prev;
                      return {
                        ...prev,
                        cart_items: prev.cart_items.map((cartItem) =>
                          cartItem.cart_item_id === item.cart_item_id
                            ? { ...cartItem, quantity: value }
                            : cartItem
                        ),
                      };
                    });
                  }}
                />
              </label>
              <div>
                <button type="button" onClick={() => handleUpdateCartItem(item)}>
                  Update
                </button>
                <button type="button" className="danger" onClick={() => handleRemoveCartItem(item.cart_item_id)}>
                  Remove
                </button>
              </div>
            </div>
          </article>
        ))}
      </div>
    );
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>GOAT Food App</h1>
        <p>Login/logout connects your React UI to the FastAPI authentication endpoints.</p>
      </header>

      <main className="app-main">
        <section className="card auth-card">
          <h2>Authentication</h2>
          {auth ? (
            <div className="auth-details">
              <p>
                Logged in as <strong>{auth.user_id}</strong> (<em>{auth.role}</em>)
              </p>
              <p>Token expires: {new Date(auth.expires).toLocaleString()}</p>
              <button type="button" onClick={handleLogout}>Logout</button>
            </div>
          ) : (
            <form className="login-form" onSubmit={handleLogin}>
              <label>
                Email
                <input
                  type="email"
                  value={loginEmail}
                  onChange={(event) => setLoginEmail(event.target.value)}
                  required
                  placeholder="you@example.com"
                />
              </label>
              <label>
                Password
                <input
                  type="password"
                  value={loginPassword}
                  onChange={(event) => setLoginPassword(event.target.value)}
                  required
                  placeholder="Enter password"
                />
              </label>
              <button type="submit">Login</button>
              {authError && <p className="error-text">{authError}</p>}
            </form>
          )}
        </section>

        <section className="card grid-card">
          <div>
            <h2>Food Catalog</h2>
            {loadingFood && <p>Loading food items...</p>}
            {foodError && <p className="error-text">{foodError}</p>}
            {!loadingFood && !foodError && foodItems.length === 0 && <p>No food items found.</p>}
            {!loadingFood && !foodError && foodItems.length > 0 && (
              <div className="food-grid">
                {foodItems.map((item) => {
                  const itemId = item.food_item_id ?? item.id;
                  return (
                    <article key={itemId} className="food-card">
                      <h3>{item.food_name ?? item.name ?? 'Unnamed item'}</h3>
                      <p><strong>Restaurant:</strong> {item.restaurant_id}</p>
                      <p><strong>Price:</strong> ${formatMoney(item.price)}</p>
                      <p><strong>Course:</strong> {item.course}</p>
                      <div className="food-actions">
                        <label>
                          Qty
                          <input
                            type="number"
                            min="1"
                            value={cartQuantities[itemId] || 1}
                            onChange={(event) => handleQuantityChange(itemId, event.target.value)}
                          />
                        </label>
                        <button type="button" onClick={() => handleAddToCart(itemId)}>
                          Add to cart
                        </button>
                      </div>
                    </article>
                  );
                })}
              </div>
            )}
          </div>

          <div className="cart-card">
            <h2>Cart</h2>
            {loadingCart && <p>Loading cart...</p>}
            {cartError && <p className="error-text">{cartError}</p>}
            {!loadingCart && renderCartItems()}
            {cart && cart.cart_items?.length > 0 && (
              <div className="cart-summary">
                <p><strong>Total:</strong> ${formatMoney(cart.total)}</p>
              </div>
            )}
          </div>
        </section>

        <section className="card">
          <h2>Restaurant Directory</h2>
          {loadingRestaurants && <p>Loading restaurants...</p>}
          {restaurantError && <p className="error-text">{restaurantError}</p>}
          {!loadingRestaurants && !restaurantError && restaurants.length === 0 && (
            <p>No restaurants found. Add some to the backend or check the API.</p>)}
          {!loadingRestaurants && !restaurantError && restaurants.length > 0 && (
            <div className="restaurant-list">
              {restaurants.map((restaurant) => (
                <article key={restaurant.restaurant_id} className="restaurant-card">
                  <h3>{restaurant.restaurant_name}</h3>
                  <p><strong>Cuisine:</strong> {restaurant.cuisine}</p>
                  <p><strong>Address:</strong> {restaurant.address}</p>
                  <p>
                    <strong>Hours:</strong> {restaurant.open_hour} - {restaurant.closed_hour}
                  </p>
                  <p><strong>Status:</strong> {restaurant.restaurant_status}</p>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
