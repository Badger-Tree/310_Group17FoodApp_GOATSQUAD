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
  const [signupFirstName, setSignupFirstName] = useState('');
  const [signupLastName, setSignupLastName] = useState('');
  const [signupEmail, setSignupEmail] = useState('');
  const [signupPassword, setSignupPassword] = useState('');
  const [signupRole, setSignupRole] = useState('CUSTOMER');
  const [signupError, setSignupError] = useState('');
  const [signupMessage, setSignupMessage] = useState('');
  const [addresses, setAddresses] = useState([]);
  const [selectedAddressId, setSelectedAddressId] = useState('');
  const [newAddressStreet, setNewAddressStreet] = useState('');
  const [newAddressCity, setNewAddressCity] = useState('');
  const [newAddressPostalCode, setNewAddressPostalCode] = useState('');
  const [newAddressInstructions, setNewAddressInstructions] = useState('');
  const [addressMessage, setAddressMessage] = useState('');
  const [orderError, setOrderError] = useState('');
  const [orderSuccess, setOrderSuccess] = useState('');
  const [favorites, setFavorites] = useState([]);
  const [loadingFavorites, setLoadingFavorites] = useState(false);
  const [favoritesError, setFavoritesError] = useState('');
  const [orders, setOrders] = useState([]);
  const [loadingOrders, setLoadingOrders] = useState(false);
  const [ordersError, setOrdersError] = useState('');
  const [inventory, setInventory] = useState({});
  const [loadingInventory, setLoadingInventory] = useState(false);
  const [inventoryError, setInventoryError] = useState('');
  const [foodItemsManagement, setFoodItemsManagement] = useState([]);
  const [loadingFoodManagement, setLoadingFoodManagement] = useState(false);
  const [foodManagementError, setFoodManagementError] = useState('');
  const [showCreateFoodForm, setShowCreateFoodForm] = useState(false);
  const [editingFoodItem, setEditingFoodItem] = useState(null);
  const [newFoodName, setNewFoodName] = useState('');
  const [newFoodRestaurantId, setNewFoodRestaurantId] = useState('');
  const [newFoodPrice, setNewFoodPrice] = useState('');
  const [newFoodDescription, setNewFoodDescription] = useState('');
  const [newFoodCourse, setNewFoodCourse] = useState('');
  const [selectedRestaurantId, setSelectedRestaurantId] = useState(null);
  const selectedRestaurant = restaurants.find((restaurant) => String(restaurant.restaurant_id) === String(selectedRestaurantId)) || null;
  const restaurantFoodItems = selectedRestaurant
    ? foodItems.filter((item) => String(item.restaurant_id) === String(selectedRestaurant.restaurant_id))
    : foodItems;
  const [auth, setAuth] = useState(() => {
    if (typeof window === 'undefined') {
      return null;
    }
    const saved = localStorage.getItem(AUTH_STORAGE_KEY);
    const parsed = saved ? JSON.parse(saved) : null;
    console.log('Initial auth state:', parsed);
    return parsed;
  });

  useEffect(() => {
    console.log('Auth state in useEffect:', auth);
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
      setAddresses([]);
      setSelectedAddressId('');
      setFavorites([]);
      return;
    }

    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(auth));
    if (auth.user_id) {
      loadCart(auth.user_id);
      loadAddresses(auth.user_id);
      loadFavorites();
      loadOrders();
      if (auth.role === 'STAFF') {
        loadFoodItemsManagement();
      }
    }
  }, [auth]);

  const authHeaders = () => ({
    token: auth?.token || '',
    'Content-Type': 'application/json',
  });

  const loadFavorites = async () => {
    if (!auth?.token) return;
    setLoadingFavorites(true);
    setFavoritesError('');

    try {
      const response = await fetch(`${API_BASE_URL}/favorites/me`, {
        headers: authHeaders(),
      });
      if (!response.ok) {
        throw new Error(`Unable to load favorites (${response.status})`);
      }
      const data = await response.json();
      setFavorites(Array.isArray(data) ? data : []);
    } catch (err) {
      setFavoritesError(err.message);
      setFavorites([]);
    } finally {
      setLoadingFavorites(false);
    }
  };

  const isRestaurantFavorite = (restaurantId) =>
    favorites.some((fav) => String(fav.restaurant_id) === String(restaurantId));

  const handleToggleRestaurantFavorite = async (restaurantId, currentlyFavorite) => {
    if (!auth?.token) {
      setFavoritesError('Please log in to manage favorites.');
      return;
    }

    setFavoritesError('');
    const method = currentlyFavorite ? 'DELETE' : 'POST';
    try {
      const response = await fetch(
        `${API_BASE_URL}/favorites/RESTAURANT/${encodeURIComponent(restaurantId)}`,
        {
          method,
          headers: authHeaders(),
        }
      );

      if (!response.ok && !(method === 'DELETE' && response.status === 204)) {
        const body = await response.text();
        throw new Error(`Favorite update failed (${response.status}) ${body}`);
      }
      await loadFavorites();
    } catch (err) {
      setFavoritesError(err.message);
    }
  };

  const loadOrders = async () => {
    if (!auth?.token) return;
    setLoadingOrders(true);
    setOrdersError('');

    try {
      const response = await fetch(`${API_BASE_URL}/orders/get_order_by_user/${encodeURIComponent(auth.user_id)}`, {
        headers: authHeaders(),
      });
      if (!response.ok) {
        throw new Error(`Unable to load orders (${response.status})`);
      }
      const data = await response.json();
      setOrders(Array.isArray(data) ? data : []);
    } catch (err) {
      setOrdersError(err.message);
      setOrders([]);
    } finally {
      setLoadingOrders(false);
    }
  };

  const handleCancelOrder = async (orderId) => {
    if (!auth?.token) {
      setOrdersError('Please log in to manage orders.');
      return;
    }

    setOrdersError('');
    try {
      const response = await fetch(`${API_BASE_URL}/orders/cancel_order_customer/${encodeURIComponent(orderId)}`, {
        method: 'PUT',
        headers: authHeaders(),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Cancel order failed (${response.status}) ${body}`);
      }
      await loadOrders();
    } catch (err) {
      setOrdersError(err.message);
    }
  };

  const handleAcceptOrder = async (orderId) => {
    if (!auth?.token) {
      setOrdersError('Please log in to manage orders.');
      return;
    }

    setOrdersError('');
    try {
      const response = await fetch(`${API_BASE_URL}/orders/accept_order/${encodeURIComponent(orderId)}`, {
        method: 'PUT',
        headers: authHeaders(),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Accept order failed (${response.status}) ${body}`);
      }
      await loadOrders();
    } catch (err) {
      setOrdersError(err.message);
    }
  };

  const handleCancelOrderStaff = async (orderId) => {
    if (!auth?.token) {
      setOrdersError('Please log in to manage orders.');
      return;
    }

    setOrdersError('');
    try {
      const response = await fetch(`${API_BASE_URL}/orders/cancel_order_restaurant/${encodeURIComponent(orderId)}`, {
        method: 'PUT',
        headers: authHeaders(),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Cancel order failed (${response.status}) ${body}`);
      }
      await loadOrders();
    } catch (err) {
      setOrdersError(err.message);
    }
  };

  const loadInventoryForFoodItem = async (foodItemId) => {
    if (!auth?.token) return;
    setLoadingInventory(true);
    setInventoryError('');

    try {
      const response = await fetch(`${API_BASE_URL}/inventory/${encodeURIComponent(foodItemId)}`, {
        headers: authHeaders(),
      });
      if (!response.ok) {
        if (response.status === 404) {
          setInventory((prev) => ({ ...prev, [foodItemId]: null }));
          return;
        }
        throw new Error(`Unable to load inventory (${response.status})`);
      }
      const data = await response.json();
      setInventory((prev) => ({ ...prev, [foodItemId]: data }));
    } catch (err) {
      setInventoryError(err.message);
      setInventory((prev) => ({ ...prev, [foodItemId]: null }));
    } finally {
      setLoadingInventory(false);
    }
  };

  const handleUpdateInventory = async (foodItemId, newQuantity) => {
    if (!auth?.token) {
      setInventoryError('Please log in to manage inventory.');
      return;
    }

    setInventoryError('');
    try {
      const response = await fetch(`${API_BASE_URL}/inventory/${encodeURIComponent(foodItemId)}`, {
        method: 'PATCH',
        headers: authHeaders(),
        body: JSON.stringify({ quantity: newQuantity }),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Update inventory failed (${response.status}) ${body}`);
      }
      const updatedInventory = await response.json();
      setInventory((prev) => ({ ...prev, [foodItemId]: updatedInventory }));
    } catch (err) {
      setInventoryError(err.message);
    }
  };

  const handleToggleOrderFavorite = async (orderId, currentlyFavorite) => {
    if (!auth?.token) {
      setFavoritesError('Please log in to manage favorites.');
      return;
    }

    setFavoritesError('');
    const method = currentlyFavorite ? 'DELETE' : 'POST';
    try {
      const response = await fetch(
        `${API_BASE_URL}/favorites/ORDER/${encodeURIComponent(orderId)}`,
        {
          method,
          headers: authHeaders(),
        }
      );

      if (!response.ok && !(method === 'DELETE' && response.status === 204)) {
        const body = await response.text();
        throw new Error(`Favorite update failed (${response.status}) ${body}`);
      }
      await loadFavorites();
    } catch (err) {
      setFavoritesError(err.message);
    }
  };

  const isOrderFavorite = (orderId) =>
    favorites.some((fav) => String(fav.order_id) === String(orderId));

  const loadFoodItemsManagement = async () => {
    if (!auth?.token) return;
    setLoadingFoodManagement(true);
    setFoodManagementError('');

    try {
      const response = await fetch(`${API_BASE_URL}/food-items`, {
        headers: authHeaders(),
      });
      if (!response.ok) {
        throw new Error(`Unable to load food items (${response.status})`);
      }
      const data = await response.json();
      setFoodItemsManagement(Array.isArray(data) ? data : []);
    } catch (err) {
      setFoodManagementError(err.message);
      setFoodItemsManagement([]);
    } finally {
      setLoadingFoodManagement(false);
    }
  };

  const handleCreateFoodItem = async (event) => {
    event.preventDefault();
    if (!auth?.token) {
      setFoodManagementError('Please log in to manage food items.');
      return;
    }

    setFoodManagementError('');
    try {
      const response = await fetch(`${API_BASE_URL}/food-items`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({
          food_name: newFoodName,
          restaurant_id: parseInt(newFoodRestaurantId),
          price: parseFloat(newFoodPrice),
          description: newFoodDescription,
          course: newFoodCourse,
        }),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Create food item failed (${response.status}) ${body}`);
      }

      const newFoodItem = await response.json();
      setFoodItemsManagement((prev) => [...prev, newFoodItem]);
      setFoodItems((prev) => [...prev, newFoodItem]);

      // Reset form
      setNewFoodName('');
      setNewFoodRestaurantId('');
      setNewFoodPrice('');
      setNewFoodDescription('');
      setNewFoodCourse('');
      setShowCreateFoodForm(false);
    } catch (err) {
      setFoodManagementError(err.message);
    }
  };

  const handleUpdateFoodItem = async (event) => {
    event.preventDefault();
    if (!auth?.token || !editingFoodItem) {
      setFoodManagementError('Please log in to manage food items.');
      return;
    }

    setFoodManagementError('');
    try {
      const response = await fetch(`${API_BASE_URL}/food-items/${editingFoodItem.food_item_id}`, {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify({
          food_name: newFoodName,
          price: parseFloat(newFoodPrice),
          description: newFoodDescription,
          course: newFoodCourse,
        }),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Update food item failed (${response.status}) ${body}`);
      }

      const updatedFoodItem = await response.json();
      setFoodItemsManagement((prev) =>
        prev.map((item) =>
          item.food_item_id === editingFoodItem.food_item_id ? updatedFoodItem : item
        )
      );
      setFoodItems((prev) =>
        prev.map((item) =>
          item.food_item_id === editingFoodItem.food_item_id ? updatedFoodItem : item
        )
      );

      // Reset form
      setEditingFoodItem(null);
      setNewFoodName('');
      setNewFoodPrice('');
      setNewFoodDescription('');
      setNewFoodCourse('');
    } catch (err) {
      setFoodManagementError(err.message);
    }
  };

  const handleDeleteFoodItem = async (foodItemId) => {
    if (!auth?.token) {
      setFoodManagementError('Please log in to manage food items.');
      return;
    }

    if (!confirm('Are you sure you want to delete this food item?')) {
      return;
    }

    setFoodManagementError('');
    try {
      const response = await fetch(`${API_BASE_URL}/food-items/${foodItemId}`, {
        method: 'DELETE',
        headers: authHeaders(),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Delete food item failed (${response.status}) ${body}`);
      }

      setFoodItemsManagement((prev) =>
        prev.filter((item) => item.food_item_id !== foodItemId)
      );
      setFoodItems((prev) =>
        prev.filter((item) => item.food_item_id !== foodItemId)
      );
    } catch (err) {
      setFoodManagementError(err.message);
    }
  };

  const handleEditFoodItem = (foodItem) => {
    setEditingFoodItem(foodItem);
    setNewFoodName(foodItem.food_name);
    setNewFoodPrice(foodItem.price.toString());
    setNewFoodDescription(foodItem.description);
    setNewFoodCourse(foodItem.course);
  };

  const handleCancelEdit = () => {
    setEditingFoodItem(null);
    setNewFoodName('');
    setNewFoodPrice('');
    setNewFoodDescription('');
    setNewFoodCourse('');
  };

  const handleSelectRestaurant = (restaurantId) => {
    setSelectedRestaurantId(restaurantId);
  };

  const handleClearSelectedRestaurant = () => {
    setSelectedRestaurantId(null);
  };

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

  const loadAddresses = async (customerId) => {
    if (!customerId) return;
    try {
      const response = await fetch(`${API_BASE_URL}/addresses/by-customer/${encodeURIComponent(customerId)}`);
      if (!response.ok) {
        throw new Error(`Unable to load addresses (${response.status})`);
      }
      const data = await response.json();
      setAddresses(Array.isArray(data) ? data : []);
      if (Array.isArray(data) && data.length > 0) {
        setSelectedAddressId(data[0].address_id);
      }
    } catch (err) {
      console.warn(`Address load failed: ${err.message}`);
      setAddresses([]);
      setSelectedAddressId('');
    }
  };

  const handleAddNewAddress = async (event) => {
    event.preventDefault();
    setAddressMessage('');
    setOrderError('');
    setOrderSuccess('');

    if (!auth?.token) {
      setAddressMessage('Please log in before adding an address.');
      return;
    }

    if (!newAddressStreet.trim() || !newAddressCity.trim() || !newAddressPostalCode.trim()) {
      setAddressMessage('Street, city, and postal code are required.');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/addresses/new`, {
        method: 'POST',
        headers: {
          token: auth.token,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          street: newAddressStreet,
          city: newAddressCity,
          postal_code: newAddressPostalCode,
          instructions: newAddressInstructions || null,
        }),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Adding address failed (${response.status}) ${body}`);
      }

      const newAddress = await response.json();
      const updatedAddresses = [...addresses, newAddress];
      setAddresses(updatedAddresses);
      setSelectedAddressId(newAddress.address_id);
      setNewAddressStreet('');
      setNewAddressCity('');
      setNewAddressPostalCode('');
      setNewAddressInstructions('');
      setAddressMessage('Address added. Ready to submit order.');
    } catch (err) {
      setAddressMessage(err.message);
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

  const handleSignup = async (event) => {
    event.preventDefault();
    setSignupError('');
    setSignupMessage('');

    const endpoint = signupRole === 'STAFF' ? '/users/new-staff' : '/users/new-customer';
    const payload = {
      email: signupEmail,
      first_name: signupFirstName,
      last_name: signupLastName,
      password: signupPassword,
    };

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Signup failed (${response.status}) ${body}`);
      }

      const createdUser = await response.json();
      setSignupMessage(`Account created for ${createdUser.email} as ${createdUser.role}. Logging in...`);
      setSignupFirstName('');
      setSignupLastName('');
      setSignupEmail('');
      setSignupPassword('');
      setSignupRole('CUSTOMER');

      const loginResponse = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: createdUser.email, password: payload.password }),
      });

      if (!loginResponse.ok) {
        const body = await loginResponse.text();
        throw new Error(`Signup succeeded but login failed (${loginResponse.status}) ${body}`);
      }

      const authData = await loginResponse.json();
      setAuth(authData);
      setSignupMessage(`Account created and logged in as ${createdUser.role}.`);
    } catch (err) {
      setSignupError(err.message);
    }
  };

  const handleSubmitOrder = async () => {
    setOrderError('');
    setOrderSuccess('');
    setAddressMessage('');

    if (!auth?.token) {
      setOrderError('Please log in before submitting an order.');
      return;
    }

    if (!selectedAddressId.trim()) {
      setOrderError('Please choose an address or add a new one before submitting the order.');
      return;
    }

    if (!cart?.cart_items || cart.cart_items.length === 0) {
      setOrderError('Your cart is empty. Add items before submitting an order.');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/orders/create_order/${encodeURIComponent(selectedAddressId)}`, {
        method: 'POST',
        headers: { token: auth.token },
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Order submission failed (${response.status}) ${body}`);
      }

      const orderData = await response.json();
      setOrderSuccess(`Order ${orderData.order_id} created successfully! Status: ${orderData.status}`);
      await loadCart(auth.user_id);
    } catch (err) {
      setOrderError(err.message);
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

  const cartHasItems = cart?.cart_items?.length > 0;

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
            <>
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

              <div className="signup-section">
                <h3>Create an account</h3>
                <form className="signup-form" onSubmit={handleSignup}>
                  <label>
                    First Name
                    <input
                      type="text"
                      value={signupFirstName}
                      onChange={(event) => setSignupFirstName(event.target.value)}
                      required
                      placeholder="First name"
                    />
                  </label>
                  <label>
                    Last Name
                    <input
                      type="text"
                      value={signupLastName}
                      onChange={(event) => setSignupLastName(event.target.value)}
                      required
                      placeholder="Last name"
                    />
                  </label>
                  <label>
                    Email
                    <input
                      type="email"
                      value={signupEmail}
                      onChange={(event) => setSignupEmail(event.target.value)}
                      required
                      placeholder="you@example.com"
                    />
                  </label>
                  <label>
                    Password
                    <input
                      type="password"
                      value={signupPassword}
                      onChange={(event) => setSignupPassword(event.target.value)}
                      required
                      placeholder="Create a password"
                    />
                  </label>
                  <label>
                    Account Type
                    <select value={signupRole} onChange={(event) => setSignupRole(event.target.value)}>
                      <option value="CUSTOMER">Customer</option>
                      <option value="STAFF">Staff</option>
                    </select>
                  </label>
                  <button type="submit">Create account</button>
                </form>
                {signupError && <p className="error-text">{signupError}</p>}
                {signupMessage && <p className="success-text">{signupMessage}</p>}
              </div>
            </>
          )}
        </section>

        <section className="card grid-card">
          <div>
            <div className="food-header-row">
              <h2>{selectedRestaurant ? `${selectedRestaurant.restaurant_name} Menu` : 'Food Catalog'}</h2>
              {selectedRestaurant && (
                <button type="button" className="secondary" onClick={handleClearSelectedRestaurant}>
                  Back to restaurants
                </button>
              )}
            </div>
            {loadingFood && <p>Loading food items...</p>}
            {foodError && <p className="error-text">{foodError}</p>}
            {!loadingFood && !foodError && restaurantFoodItems.length === 0 && (
              <p>{selectedRestaurant ? 'No items found for this restaurant.' : 'No food items found.'}</p>
            )}
            {!loadingFood && !foodError && restaurantFoodItems.length > 0 && (
              <div className="food-grid">
                {restaurantFoodItems.map((item) => {
                  const itemId = item.food_item_id ?? item.id;
                  return (
                    <article key={itemId} className="food-card">
                      <h3>{item.food_name ?? item.name ?? 'Unnamed item'}</h3>
                      {selectedRestaurant ? null : (
                        <p><strong>Restaurant:</strong> {item.restaurant_id}</p>
                      )}
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
            {cartHasItems && (
              <>
                <div className="cart-summary">
                  <h3>Order summary</h3>
                  <p><strong>Total:</strong> ${formatMoney(cart.total)}</p>
                </div>
                <div className="checkout-panel">
                  <h3>Delivery address</h3>
                  {addresses.length > 0 ? (
                    <label>
                      Choose existing address
                      <select
                        value={selectedAddressId}
                        onChange={(event) => setSelectedAddressId(event.target.value)}
                      >
                        {addresses.map((address) => (
                          <option key={address.address_id} value={address.address_id}>
                            {`${address.street}, ${address.city}, ${address.postal_code}`}
                          </option>
                        ))}
                      </select>
                    </label>
                  ) : (
                    <p>No saved addresses found. Add one below.</p>
                  )}

                  <div className="new-address-form">
                    <h4>Add a new address</h4>
                    <label>
                      Street
                      <input
                        type="text"
                        value={newAddressStreet}
                        onChange={(event) => setNewAddressStreet(event.target.value)}
                        placeholder="Street"
                      />
                    </label>
                    <label>
                      City
                      <input
                        type="text"
                        value={newAddressCity}
                        onChange={(event) => setNewAddressCity(event.target.value)}
                        placeholder="City"
                      />
                    </label>
                    <label>
                      Postal code
                      <input
                        type="text"
                        value={newAddressPostalCode}
                        onChange={(event) => setNewAddressPostalCode(event.target.value)}
                        placeholder="Postal code"
                      />
                    </label>
                    <label>
                      Instructions
                      <input
                        type="text"
                        value={newAddressInstructions}
                        onChange={(event) => setNewAddressInstructions(event.target.value)}
                        placeholder="Delivery instructions (optional)"
                      />
                    </label>
                    <button type="button" onClick={handleAddNewAddress}>
                      Save address
                    </button>
                    {addressMessage && <p className="success-text">{addressMessage}</p>}
                  </div>

                  <button type="button" onClick={handleSubmitOrder}>
                    Submit order
                  </button>
                  {orderError && <p className="error-text">{orderError}</p>}
                  {orderSuccess && <p className="success-text">{orderSuccess}</p>}
                </div>
              </>
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
                <article
                  key={restaurant.restaurant_id}
                  className={`restaurant-card${selectedRestaurantId === String(restaurant.restaurant_id) ? ' selected' : ''}`}
                >
                  <h3>{restaurant.restaurant_name}</h3>
                  <p><strong>Cuisine:</strong> {restaurant.cuisine}</p>
                  <p><strong>Address:</strong> {restaurant.address}</p>
                  <p>
                    <strong>Hours:</strong> {restaurant.open_hour} - {restaurant.closed_hour}
                  </p>
                  <p><strong>Status:</strong> {restaurant.restaurant_status}</p>
                  <div className="restaurant-card-actions">
                    <button type="button" onClick={() => handleSelectRestaurant(restaurant.restaurant_id)}>
                      View menu
                    </button>
                    <button
                      type="button"
                      className={`favorite-button ${isRestaurantFavorite(restaurant.restaurant_id) ? 'favorited' : ''}`}
                      onClick={() => handleToggleRestaurantFavorite(restaurant.restaurant_id, isRestaurantFavorite(restaurant.restaurant_id))}
                    >
                      {isRestaurantFavorite(restaurant.restaurant_id) ? 'Unfavorite' : 'Add favorite'}
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <section className="card">
          <h2>Your Favorite Restaurants</h2>
          {!auth && <p>Log in to save favorite restaurants and manage them here.</p>}
          {auth && loadingFavorites && <p>Loading favorites...</p>}
          {auth && favoritesError && <p className="error-text">{favoritesError}</p>}
          {auth && !loadingFavorites && favorites.filter((fav) => fav.restaurant_id).length === 0 && (
            <p>You have no favorite restaurants yet. Use the button on any restaurant card to add one.</p>
          )}
          {auth && !loadingFavorites && favorites.filter((fav) => fav.restaurant_id).length > 0 && (
            <div className="favorite-list">
              {favorites
                .filter((fav) => fav.restaurant_id)
                .map((restaurant) => (
                  <article key={restaurant.restaurant_id} className="favorite-card">
                    <h3>{restaurant.restaurant_name}</h3>
                    <p><strong>Cuisine:</strong> {restaurant.cuisine}</p>
                    <p><strong>Address:</strong> {restaurant.address}</p>
                    <div className="favorite-actions">
                      <button type="button" onClick={() => handleSelectRestaurant(restaurant.restaurant_id)}>
                        View menu
                      </button>
                      <button
                        type="button"
                        className="favorite-button favorited"
                        onClick={() => handleToggleRestaurantFavorite(restaurant.restaurant_id, true)}
                      >
                        Remove favorite
                      </button>
                    </div>
                  </article>
                ))}
            </div>
          )}
        </section>

        <section className="card">
          <h2>My Orders</h2>
          {!auth && <p>Log in to view and manage your orders.</p>}
          {auth && loadingOrders && <p>Loading orders...</p>}
          {auth && ordersError && <p className="error-text">{ordersError}</p>}
          {auth && !loadingOrders && orders.length === 0 && (
            <p>You have no orders yet. Add items to your cart and submit an order to get started.</p>
          )}
          {auth && !loadingOrders && orders.length > 0 && (
            <div className="orders-list">
              {orders.map((order) => (
                <article key={order.order_id} className="order-card">
                  <div className="order-header">
                    <h3>Order #{order.order_id}</h3>
                    <span className={`order-status status-${order.status.toLowerCase()}`}>
                      {order.status}
                    </span>
                    <button
                      type="button"
                      className={`favorite-button ${isOrderFavorite(order.order_id) ? 'favorited' : ''}`}
                      onClick={() => handleToggleOrderFavorite(order.order_id, isOrderFavorite(order.order_id))}
                    >
                      {isOrderFavorite(order.order_id) ? 'Unfavorite' : 'Favorite'}
                    </button>
                  </div>
                  <p><strong>Restaurant:</strong> {order.restaurant_id}</p>
                  <p><strong>Total:</strong> ${formatMoney(order.total_amount)}</p>
                  <p><strong>Created:</strong> {new Date(order.created_date).toLocaleString()}</p>
                  <div className="order-items">
                    <h4>Items:</h4>
                    <ul>
                      {order.items.map((item, index) => (
                        <li key={index}>
                          {item.food_item_name} x{item.quantity} - ${formatMoney(item.price_per_item * item.quantity)}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div className="order-actions">
                    {(order.status === 'PENDING' || order.status === 'ACCEPTED') && auth.role === 'CUSTOMER' && (
                      <button type="button" className="danger" onClick={() => handleCancelOrder(order.order_id)}>
                        Cancel Order
                      </button>
                    )}
                    {order.status === 'PENDING' && auth.role === 'STAFF' && (
                      <>
                        <button type="button" onClick={() => handleAcceptOrder(order.order_id)}>
                          Accept Order
                        </button>
                        <button type="button" className="danger" onClick={() => handleCancelOrderStaff(order.order_id)}>
                          Cancel Order
                        </button>
                      </>
                    )}
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {(() => {
          console.log('Checking STAFF role:', auth?.role);
          return auth && auth.role === 'STAFF';
        })() && (
          <section className="card">
            <h2>Inventory Management</h2>
            {inventoryError && <p className="error-text">{inventoryError}</p>}
            <div className="inventory-grid">
              {foodItems.map((item) => {
                const itemId = item.food_item_id ?? item.id;
                const itemInventory = inventory[itemId];
                return (
                  <article key={itemId} className="inventory-card">
                    <h3>{item.food_name ?? item.name ?? 'Unnamed item'}</h3>
                    <p><strong>Restaurant:</strong> {item.restaurant_id}</p>
                    <p><strong>Price:</strong> ${formatMoney(item.price)}</p>
                    <div className="inventory-controls">
                      <label>
                        Current Stock
                        <input
                          type="number"
                          min="0"
                          value={itemInventory?.quantity ?? 0}
                          onChange={(event) => {
                            const newQuantity = Math.max(0, Number(event.target.value) || 0);
                            if (itemInventory) {
                              handleUpdateInventory(itemId, newQuantity);
                            }
                          }}
                        />
                      </label>
                      {!itemInventory && (
                        <button
                          type="button"
                          onClick={() => loadInventoryForFoodItem(itemId)}
                        >
                          Load Inventory
                        </button>
                      )}
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        )}

        {auth && auth.role === 'STAFF' && (
          <section className="card">
            <div className="food-management-header">
              <h2>Food Item Management</h2>
              <button
                type="button"
                onClick={() => setShowCreateFoodForm(!showCreateFoodForm)}
              >
                {showCreateFoodForm ? 'Cancel' : 'Add New Food Item'}
              </button>
            </div>

            {foodManagementError && <p className="error-text">{foodManagementError}</p>}

            {showCreateFoodForm && (
              <form className="food-form" onSubmit={handleCreateFoodItem}>
                <h3>Create New Food Item</h3>
                <div className="form-grid">
                  <label>
                    Name
                    <input
                      type="text"
                      value={newFoodName}
                      onChange={(event) => setNewFoodName(event.target.value)}
                      required
                      placeholder="Food item name"
                    />
                  </label>
                  <label>
                    Restaurant ID
                    <select
                      value={newFoodRestaurantId}
                      onChange={(event) => setNewFoodRestaurantId(event.target.value)}
                      required
                    >
                      <option value="">Select Restaurant</option>
                      {restaurants.map((restaurant) => (
                        <option key={restaurant.restaurant_id} value={restaurant.restaurant_id}>
                          {restaurant.restaurant_name}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Price
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      value={newFoodPrice}
                      onChange={(event) => setNewFoodPrice(event.target.value)}
                      required
                      placeholder="0.00"
                    />
                  </label>
                  <label>
                    Course
                    <select
                      value={newFoodCourse}
                      onChange={(event) => setNewFoodCourse(event.target.value)}
                      required
                    >
                      <option value="">Select Course</option>
                      <option value="Appetizer">Appetizer</option>
                      <option value="Main">Main</option>
                      <option value="Dessert">Dessert</option>
                      <option value="Beverage">Beverage</option>
                    </select>
                  </label>
                </div>
                <label>
                  Description
                  <textarea
                    value={newFoodDescription}
                    onChange={(event) => setNewFoodDescription(event.target.value)}
                    required
                    placeholder="Food item description"
                    rows="3"
                  />
                </label>
                <div className="form-actions">
                  <button type="submit">Create Food Item</button>
                  <button type="button" onClick={() => setShowCreateFoodForm(false)}>
                    Cancel
                  </button>
                </div>
              </form>
            )}

            {editingFoodItem && (
              <form className="food-form" onSubmit={handleUpdateFoodItem}>
                <h3>Edit Food Item: {editingFoodItem.food_name}</h3>
                <div className="form-grid">
                  <label>
                    Name
                    <input
                      type="text"
                      value={newFoodName}
                      onChange={(event) => setNewFoodName(event.target.value)}
                      required
                    />
                  </label>
                  <label>
                    Price
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      value={newFoodPrice}
                      onChange={(event) => setNewFoodPrice(event.target.value)}
                      required
                    />
                  </label>
                  <label>
                    Course
                    <select
                      value={newFoodCourse}
                      onChange={(event) => setNewFoodCourse(event.target.value)}
                      required
                    >
                      <option value="Appetizer">Appetizer</option>
                      <option value="Main">Main</option>
                      <option value="Dessert">Dessert</option>
                      <option value="Beverage">Beverage</option>
                    </select>
                  </label>
                </div>
                <label>
                  Description
                  <textarea
                    value={newFoodDescription}
                    onChange={(event) => setNewFoodDescription(event.target.value)}
                    required
                    rows="3"
                  />
                </label>
                <div className="form-actions">
                  <button type="submit">Update Food Item</button>
                  <button type="button" onClick={handleCancelEdit}>
                    Cancel
                  </button>
                </div>
              </form>
            )}

            <div className="food-management-grid">
              {loadingFoodManagement && <p>Loading food items...</p>}
              {!loadingFoodManagement && foodItemsManagement.length === 0 && (
                <p>No food items found.</p>
              )}
              {!loadingFoodManagement && foodItemsManagement.length > 0 && (
                foodItemsManagement.map((item) => (
                  <article key={item.food_item_id} className="food-management-card">
                    <div className="food-info">
                      <h3>{item.food_name}</h3>
                      <p><strong>Restaurant:</strong> {restaurants.find(r => r.restaurant_id === item.restaurant_id)?.restaurant_name || item.restaurant_id}</p>
                      <p><strong>Price:</strong> ${formatMoney(item.price)}</p>
                      <p><strong>Course:</strong> {item.course}</p>
                      <p><strong>Description:</strong> {item.description}</p>
                    </div>
                    <div className="food-actions">
                      <button type="button" onClick={() => handleEditFoodItem(item)}>
                        Edit
                      </button>
                      <button
                        type="button"
                        className="danger"
                        onClick={() => handleDeleteFoodItem(item.food_item_id)}
                      >
                        Delete
                      </button>
                    </div>
                  </article>
                ))
              )}
            </div>
          </section>
        )}

        <section className="card">
          <h2>Your Favorite Orders</h2>
          {!auth && <p>Log in to save favorite orders and manage them here.</p>}
          {auth && loadingFavorites && <p>Loading favorites...</p>}
          {auth && favoritesError && <p className="error-text">{favoritesError}</p>}
          {auth && !loadingFavorites && favorites.filter((fav) => fav.order_id).length === 0 && (
            <p>You have no favorite orders yet. Use the favorite button on any order to add one.</p>
          )}
          {auth && !loadingFavorites && favorites.filter((fav) => fav.order_id).length > 0 && (
            <div className="favorite-orders-list">
              {favorites
                .filter((fav) => fav.order_id)
                .map((order) => (
                  <article key={order.order_id} className="favorite-order-card">
                    <div className="order-header">
                      <h3>Order #{order.order_id}</h3>
                      <span className={`order-status status-${order.status.toLowerCase()}`}>
                        {order.status}
                      </span>
                      <button
                        type="button"
                        className="favorite-button favorited"
                        onClick={() => handleToggleOrderFavorite(order.order_id, true)}
                      >
                        Remove favorite
                      </button>
                    </div>
                    <p><strong>Restaurant:</strong> {order.restaurant_id}</p>
                    <p><strong>Total:</strong> ${formatMoney(order.total_amount)}</p>
                    <p><strong>Created:</strong> {new Date(order.created_date).toLocaleString()}</p>
                    <div className="order-items">
                      <h4>Items:</h4>
                      <ul>
                        {order.items.map((item, index) => (
                          <li key={index}>
                            {item.food_item_name} x{item.quantity} - ${formatMoney(item.price_per_item * item.quantity)}
                          </li>
                        ))}
                      </ul>
                    </div>
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
