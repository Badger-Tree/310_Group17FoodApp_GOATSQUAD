
import { useEffect, useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
const AUTH_STORAGE_KEY = 'goat-food-auth';

function formatMoney(value) {
  const number = Number(value);
  return Number.isNaN(number) ? '-' : number.toFixed(2);
}

function App() {
  // --- Review form state and handlers for completed orders ---
  const [reviewForms, setReviewForms] = useState({});
  const handleOpenReviewForm = (orderId) => {
    setReviewForms((prev) => ({
      ...prev,
      [orderId]: { open: true, rating: 5, review: '', submitting: false, error: '' },
    }));
  };
  const handleCloseReviewForm = (orderId) => {
    setReviewForms((prev) => ({
      ...prev,
      [orderId]: { ...prev[orderId], open: false },
    }));
  };
  const handleReviewInputChange = (orderId, field, value) => {
    setReviewForms((prev) => ({
      ...prev,
      [orderId]: { ...prev[orderId], [field]: value },
    }));
  };
  const handleSubmitReview = async (order) => {
    const { rating, review } = reviewForms[order.order_id] || {};
    setReviewForms((prev) => ({
      ...prev,
      [order.order_id]: { ...prev[order.order_id], submitting: true, error: '' },
    }));
    try {
      const payload = {
        restaurant_id: order.restaurant_id,
        rating: Number(rating),
        review: review,
      };
      const response = await fetch(`${API_BASE_URL}/reviews/create_review/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: auth.token,
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Review failed (${response.status}) ${body}`);
      }
      setReviewForms((prev) => ({ ...prev, [order.order_id]: { ...prev[order.order_id], open: false, submitting: false } }));
      setOrderSuccess('Review submitted!');
      if (selectedRestaurantId && String(selectedRestaurantId) === String(order.restaurant_id)) {
        setLoadingReviews(true);
        setReviewError('');
        fetch(`${API_BASE_URL}/reviews/get_review_by_restaurant/${encodeURIComponent(order.restaurant_id)}`)
          .then((response) => {
            if (!response.ok) throw new Error(`Unable to load reviews (${response.status})`);
            return response.json();
          })
          .then((data) => {
            setRestaurantReviews(Array.isArray(data) ? data : []);
          })
          .catch((err) => {
            setReviewError(`Unable to load reviews. ${err.message}`);
            setRestaurantReviews([]);
          })
          .finally(() => {
            setLoadingReviews(false);
          });
      }
    } catch (err) {
      setReviewForms((prev) => ({ ...prev, [order.order_id]: { ...prev[order.order_id], submitting: false, error: err.message } }));
    }
  };
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
  const [selectedRestaurantId, setSelectedRestaurantId] = useState(null);
  const selectedRestaurant = restaurants.find((restaurant) => String(restaurant.restaurant_id) === String(selectedRestaurantId)) || null;
  const restaurantFoodItems = selectedRestaurant
    ? foodItems.filter((item) => String(item.restaurant_id) === String(selectedRestaurant.restaurant_id))
    : foodItems;
  const [showProfilePage, setShowProfilePage] = useState(false);
  // Reviews state
  const [restaurantReviews, setRestaurantReviews] = useState([]);
  const [loadingReviews, setLoadingReviews] = useState(false);
  const [reviewError, setReviewError] = useState('');
    // Fetch reviews when a restaurant is selected
    useEffect(() => {
      if (!selectedRestaurantId) {
        setRestaurantReviews([]);
        setReviewError('');
        setLoadingReviews(false);
        return;
      }
      setLoadingReviews(true);
      setReviewError('');
      fetch(`${API_BASE_URL}/reviews/get_review_by_restaurant/${encodeURIComponent(selectedRestaurantId)}`)
        .then((response) => {
          if (!response.ok) throw new Error(`Unable to load reviews (${response.status})`);
          return response.json();
        })
        .then((data) => {
          setRestaurantReviews(Array.isArray(data) ? data : []);
        })
        .catch((err) => {
          setReviewError(`Unable to load reviews. ${err.message}`);
          setRestaurantReviews([]);
        })
        .finally(() => {
          setLoadingReviews(false);
        });
    }, [selectedRestaurantId]);
  const [userProfile, setUserProfile] = useState(null);
  const [profileFirstName, setProfileFirstName] = useState('');
  const [profileLastName, setProfileLastName] = useState('');
  const [profilePassword, setProfilePassword] = useState('');
  const [profileError, setProfileError] = useState('');
  const [profileMessage, setProfileMessage] = useState('');
  const [loadingProfile, setLoadingProfile] = useState(false);
  const [loadingOrders, setLoadingOrders] = useState(false);
  const [pastOrders, setPastOrders] = useState([]);
  const [staffAssignments, setStaffAssignments] = useState([]);
  const [loadingStaffAssignments, setLoadingStaffAssignments] = useState(false);
  const [staffAssignmentError, setStaffAssignmentError] = useState('');
  const [selectedStaffRestaurantId, setSelectedStaffRestaurantId] = useState('');
  const [restaurantOrders, setRestaurantOrders] = useState([]);
  const [loadingRestaurantOrders, setLoadingRestaurantOrders] = useState(false);
  const [restaurantOrderError, setRestaurantOrderError] = useState('');
  const [orderActionMessage, setOrderActionMessage] = useState('');
  const [orderActionError, setOrderActionError] = useState('');
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
      setAddresses([]);
      setSelectedAddressId('');
      return;
    }

    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(auth));
    if (auth.user_id) {
      loadCart(auth.user_id);
      loadAddresses(auth.user_id);
      loadUserProfile(auth.user_id);
      if (auth.role === 'CUSTOMER') {
        loadPastOrders(auth.user_id);
      }
      if (auth.role === 'STAFF') {
        loadStaffAssignments(auth.user_id);
      }
    }
  }, [auth]);

  const loadStaffAssignments = async (userId) => {
    if (!userId) return;
    setLoadingStaffAssignments(true);
    setStaffAssignmentError('');

    try {
      const response = await fetch(`${API_BASE_URL}/staff-assignments/staff/${encodeURIComponent(userId)}`, {
        headers: authHeaders(),
      });
      if (!response.ok) {
        throw new Error(`Unable to load staff assignments (${response.status})`);
      }
      const data = await response.json();
      const assignments = Array.isArray(data) ? data : [];
      setStaffAssignments(assignments);
      if (assignments.length > 0 && !selectedStaffRestaurantId) {
        setSelectedStaffRestaurantId(String(assignments[0].restaurant_id));
      }
    } catch (err) {
      setStaffAssignmentError(`Unable to load staff assignments. ${err.message}`);
      setStaffAssignments([]);
    } finally {
      setLoadingStaffAssignments(false);
    }
  };

  const loadRestaurantOrders = async (restaurantId) => {
    if (!restaurantId) {
      setRestaurantOrders([]);
      return;
    }
    setLoadingRestaurantOrders(true);
    setRestaurantOrderError('');
    setOrderActionMessage('');
    setOrderActionError('');

    try {
      const response = await fetch(`${API_BASE_URL}/orders/get_order_by_restaurant/${encodeURIComponent(restaurantId)}`, {
        headers: authHeaders(),
      });
      if (!response.ok) {
        throw new Error(`Unable to load restaurant orders (${response.status})`);
      }
      const data = await response.json();
      setRestaurantOrders(Array.isArray(data) ? data : []);
    } catch (err) {
      setRestaurantOrderError(`Unable to load restaurant orders. ${err.message}`);
      setRestaurantOrders([]);
    } finally {
      setLoadingRestaurantOrders(false);
    }
  };

  useEffect(() => {
    if (auth?.role === 'STAFF' && selectedStaffRestaurantId) {
      loadRestaurantOrders(selectedStaffRestaurantId);
    } else {
      setRestaurantOrders([]);
    }
  }, [selectedStaffRestaurantId, auth]);

  const handleAcceptOrder = async (orderId) => {
    if (!auth?.token) {
      setOrderActionError('Please log in to approve orders.');
      return;
    }
    setOrderActionMessage('');
    setOrderActionError('');

    try {
      const response = await fetch(`${API_BASE_URL}/orders/accept_order/${encodeURIComponent(orderId)}`, {
        method: 'PUT',
        headers: authHeaders(),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Approve failed (${response.status}) ${body}`);
      }
      await response.json();
      setOrderActionMessage('Order approved successfully.');
      loadRestaurantOrders(selectedStaffRestaurantId);
    } catch (err) {
      setOrderActionError(err.message);
    }
  };

  const handleCancelOrderRestaurant = async (orderId) => {
    if (!auth?.token) {
      setOrderActionError('Please log in to cancel orders.');
      return;
    }
    setOrderActionMessage('');
    setOrderActionError('');

    try {
      const response = await fetch(`${API_BASE_URL}/orders/cancel_order_restaurant/${encodeURIComponent(orderId)}`, {
        method: 'PUT',
        headers: authHeaders(),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Cancel failed (${response.status}) ${body}`);
      }
      await response.json();
      setOrderActionMessage('Order canceled successfully.');
      loadRestaurantOrders(selectedStaffRestaurantId);
    } catch (err) {
      setOrderActionError(err.message);
    }
  };

  const authHeaders = () => ({
    token: auth?.token || '',
    'Content-Type': 'application/json',
  });

  const handleSelectRestaurant = (restaurantId) => {
    setSelectedRestaurantId(restaurantId);
  };

  const handleClearSelectedRestaurant = () => {
    setSelectedRestaurantId(null);
  };

  const handleOpenProfile = () => {
    setShowProfilePage(true);
  };

  const handleCloseProfile = () => {
    setShowProfilePage(false);
  };

  const loadUserProfile = async (userId) => {
    if (!userId) return;
    setLoadingProfile(true);
    setProfileError('');

    try {
      const response = await fetch(`${API_BASE_URL}/users/${encodeURIComponent(userId)}`);
      if (!response.ok) {
        throw new Error(`Unable to load profile (${response.status})`);
      }
      const data = await response.json();
      setUserProfile(data);
      setProfileFirstName(data.first_name ?? '');
      setProfileLastName(data.last_name ?? '');
      setProfilePassword('');
    } catch (err) {
      setProfileError(`Unable to load profile. ${err.message}`);
    } finally {
      setLoadingProfile(false);
    }
  };

  const loadPastOrders = async (userId) => {
    if (!userId) return;
    setLoadingOrders(true);
    setProfileError('');

    try {
      const response = await fetch(`${API_BASE_URL}/orders/get_order_by_user/${encodeURIComponent(userId)}`);
      if (!response.ok) {
        throw new Error(`Unable to load orders (${response.status})`);
      }
      const data = await response.json();
      setPastOrders(Array.isArray(data) ? data : []);
    } catch (err) {
      setProfileError(`Unable to load order history. ${err.message}`);
      setPastOrders([]);
    } finally {
      setLoadingOrders(false);
    }
  };

  const handleProfileSave = async (event) => {
    event.preventDefault();
    if (!auth?.token || !auth.user_id) {
      setProfileError('Please log in before saving your profile.');
      return;
    }

    setProfileError('');
    setProfileMessage('');

    const payload = {
      first_name: profileFirstName,
      last_name: profileLastName,
    };
    if (profilePassword.trim()) {
      payload.password = profilePassword;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/users/update-user/${encodeURIComponent(auth.user_id)}`, {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Save failed (${response.status}) ${body}`);
      }
      const updatedProfile = await response.json();
      setUserProfile(updatedProfile);
      setProfileMessage('Profile updated successfully.');
      setProfilePassword('');
    } catch (err) {
      setProfileError(err.message);
    }
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
      if (auth?.token) {
        await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: { token: auth.token },
        });
      }
    } catch (err) {
      console.warn(err);
    } finally {
      setShowProfilePage(false);
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
      if (auth?.user_id) {
        loadPastOrders(auth.user_id);
      }
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
              <div className="auth-actions-row">
                <button type="button" onClick={handleOpenProfile}>Profile</button>
                <button type="button" onClick={handleLogout}>Logout</button>
              </div>
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

        {showProfilePage ? (
          <section className="card profile-card">
            <div className="profile-header-row">
              <h2>My Profile</h2>
              <button type="button" className="secondary" onClick={handleCloseProfile}>
                Back to home
              </button>
            </div>
            {loadingProfile && <p>Loading profile...</p>}
            {profileError && <p className="error-text">{profileError}</p>}
            {!loadingProfile && (
              <form className="profile-form" onSubmit={handleProfileSave}>
                <label>
                  Email
                  <input type="email" value={userProfile?.email || ''} disabled />
                </label>
                <label>
                  First Name
                  <input
                    type="text"
                    value={profileFirstName}
                    onChange={(event) => setProfileFirstName(event.target.value)}
                    required
                  />
                </label>
                <label>
                  Last Name
                  <input
                    type="text"
                    value={profileLastName}
                    onChange={(event) => setProfileLastName(event.target.value)}
                    required
                  />
                </label>
                <label>
                  Password
                  <input
                    type="password"
                    value={profilePassword}
                    onChange={(event) => setProfilePassword(event.target.value)}
                    placeholder="Leave blank to keep current password"
                  />
                </label>
                <button type="submit">Save profile</button>
                {profileMessage && <p className="success-text">{profileMessage}</p>}
              </form>
            )}

            {auth?.role === 'STAFF' ? (
              <section className="staff-assignments-card">
                <h3>Staff assignments</h3>
                {loadingStaffAssignments && <p>Loading staff assignments...</p>}
                {staffAssignmentError && <p className="error-text">{staffAssignmentError}</p>}
                {!loadingStaffAssignments && staffAssignments.length === 0 && (
                  <p>No staff assignments found for your account.</p>
                )}
                {!loadingStaffAssignments && staffAssignments.length > 0 && (
                  <>
                    <div className="staff-assignment-list">
                      {staffAssignments.map((assignment) => (
                        <article key={assignment.assignment_id} className="assignment-card">
                          <p><strong>Assignment ID:</strong> {assignment.assignment_id}</p>
                          <p><strong>Restaurant:</strong> {assignment.restaurant_id}</p>
                          <p><strong>Role:</strong> {assignment.assignment}</p>
                        </article>
                      ))}
                    </div>

                    <div className="restaurant-order-management-card">
                      <h4>Manage restaurant orders</h4>
                      <label>
                        Select restaurant
                        <select
                          value={selectedStaffRestaurantId}
                          onChange={(event) => setSelectedStaffRestaurantId(event.target.value)}
                        >
                          {Array.from(new Set(staffAssignments.map((assignment) => String(assignment.restaurant_id)))).map((restaurantId) => (
                            <option key={restaurantId} value={restaurantId}>
                              {restaurantId}
                            </option>
                          ))}
                        </select>
                      </label>

                      {orderActionMessage && <p className="success-text">{orderActionMessage}</p>}
                      {orderActionError && <p className="error-text">{orderActionError}</p>}
                      {loadingRestaurantOrders && <p>Loading restaurant orders...</p>}
                      {restaurantOrderError && <p className="error-text">{restaurantOrderError}</p>}
                      {!loadingRestaurantOrders && !restaurantOrderError && restaurantOrders.length === 0 && (
                        <p>No orders found for this restaurant.</p>
                      )}
                      {!loadingRestaurantOrders && restaurantOrders.length > 0 && (
                        <div className="order-history-list">
                          {restaurantOrders.map((order) => (
                            <article key={order.order_id} className="order-card">
                              <p><strong>Order #</strong> {order.order_id}</p>
                              <p><strong>Status:</strong> {order.status}</p>
                              <p><strong>Placed:</strong> {new Date(order.created_date).toLocaleString()}</p>
                              <p><strong>Total:</strong> ${formatMoney(order.total_amount)}</p>
                              <p><strong>Customer:</strong> {order.customer_id}</p>
                              <p><strong>Delivery address:</strong> {order.delivery_address || order.delivery_address_id}</p>
                              {order.items && order.items.length > 0 && (
                                <div className="order-items">
                                  <h4>Items</h4>
                                  <ul>
                                    {order.items.map((item) => (
                                      <li key={`${order.order_id}-${item.food_item_id}`}>
                                        {item.quantity} x {item.food_item_id} @ ${formatMoney(item.price_per_item || item.price)}
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                              {order.status !== 'COMPLETED' && (
                                <div className="order-action-buttons">
                                  {order.status === 'PENDING' && (
                                    <button type="button" onClick={() => handleAcceptOrder(order.order_id)}>
                                      Approve
                                    </button>
                                  )}
                                  <button type="button" className="danger" onClick={() => handleCancelOrderRestaurant(order.order_id)}>
                                    Cancel
                                  </button>
                                </div>
                              )}
                              {order.status === 'COMPLETED' && (
                                <p>Order actions are not available for completed orders.</p>
                              )}
                            </article>
                          ))}
                        </div>
                      )}
                    </div>
                  </>
                )}
              </section>
            ) : (
              <section className="order-history-card">
                <h3>Past orders</h3>
                {loadingOrders && <p>Loading past orders...</p>}
                {!loadingOrders && pastOrders.length === 0 && <p>No past orders found.</p>}
                {!loadingOrders && pastOrders.length > 0 && (
                  <div className="order-history-list">
                    {pastOrders.map((order) => (
                      <article key={order.order_id} className="order-card">
                        <p><strong>Order #</strong> {order.order_id}</p>
                        <p><strong>Status:</strong> {order.status}</p>
                        <p><strong>Placed:</strong> {new Date(order.created_date).toLocaleString()}</p>
                        <p><strong>Total:</strong> ${formatMoney(order.total_amount)}</p>
                        <p><strong>Restaurant:</strong> {order.restaurant_id}</p>
                        <p><strong>Delivery address:</strong> {order.delivery_address || order.delivery_address_id}</p>
                        {order.items && order.items.length > 0 && (
                          <div className="order-items">
                            <h4>Items</h4>
                            <ul>
                              {order.items.map((item) => (
                                <li key={`${order.order_id}-${item.food_item_id}`}>
                                  {item.quantity} x {item.food_item_id} @ ${formatMoney(item.price_per_item || item.price)}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {/* Cancel button for PENDING orders */}
                        {order.status === 'PENDING' && (
                          <button
                            type="button"
                            className="danger"
                            style={{ marginTop: '0.5em' }}
                            onClick={async () => {
                              if (!auth?.token) return;
                              setOrderError('');
                              setOrderSuccess('');
                              try {
                                const response = await fetch(`${API_BASE_URL}/orders/cancel_order_customer/${encodeURIComponent(order.order_id)}`, {
                                  method: 'PUT',
                                  headers: { token: auth.token },
                                });
                                if (!response.ok) {
                                  const body = await response.text();
                                  throw new Error(`Cancel failed (${response.status}) ${body}`);
                                }
                                setOrderSuccess(`Order ${order.order_id} canceled successfully.`);
                                // Refresh orders
                                loadPastOrders(auth.user_id);
                              } catch (err) {
                                setOrderError(err.message);
                              }
                            }}
                          >
                            Cancel Order
                          </button>
                        )}
                        {/* Review form for COMPLETED orders, only if user hasn't already reviewed this restaurant */}
                        {order.status === 'COMPLETED' && (() => {
                          // Check if user has already reviewed this restaurant
                          const alreadyReviewed = restaurantReviews.some(
                            (review) => (review.user_id === auth?.user_id || review.reviewer_id === auth?.user_id) && String(review.restaurant_id) === String(order.restaurant_id)
                          );
                          if (alreadyReviewed) {
                            return <p style={{ marginTop: '0.5em', color: '#888' }}>You have already reviewed this restaurant.</p>;
                          }
                          return (
                            <div style={{ marginTop: '0.5em' }}>
                              {!(reviewForms[order.order_id]?.open) ? (
                                <button type="button" onClick={() => handleOpenReviewForm(order.order_id)}>
                                  Leave a Review
                                </button>
                              ) : (
                                <form
                                  onSubmit={e => {
                                    e.preventDefault();
                                    handleSubmitReview(order);
                                  }}
                                  style={{ marginTop: '0.5em', border: '1px solid #ccc', padding: '0.5em', borderRadius: '4px' }}
                                >
                                  <label>
                                    Rating:
                                    <select
                                      value={reviewForms[order.order_id]?.rating || 5}
                                      onChange={e => handleReviewInputChange(order.order_id, 'rating', e.target.value)}
                                      required
                                    >
                                      {[5,4,3,2,1,0].map(val => (
                                        <option key={val} value={val}>{val}</option>
                                      ))}
                                    </select>
                                  </label>
                                  <label style={{ display: 'block', marginTop: '0.5em' }}>
                                    Review:
                                    <textarea
                                      value={reviewForms[order.order_id]?.review || ''}
                                      onChange={e => handleReviewInputChange(order.order_id, 'review', e.target.value)}
                                      minLength={1}
                                      required
                                      rows={2}
                                      style={{ width: '100%' }}
                                    />
                                  </label>
                                  <div style={{ marginTop: '0.5em' }}>
                                    <button type="submit" disabled={reviewForms[order.order_id]?.submitting}>Submit Review</button>
                                    <button type="button" className="secondary" style={{ marginLeft: '0.5em' }} onClick={() => handleCloseReviewForm(order.order_id)}>
                                      Cancel
                                    </button>
                                  </div>
                                  {reviewForms[order.order_id]?.error && <p className="error-text">{reviewForms[order.order_id].error}</p>}
                                </form>
                              )}
                            </div>
                          );
                        })()}
                      </article>
                    ))}
                  </div>
                )}
              </section>
            )}
          </section>
        ) : (
          <>
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
                {/* Show reviews when a restaurant is selected */}
                {selectedRestaurant && (
                  <section className="restaurant-reviews-card">
                    <h3>Reviews</h3>
                    {loadingReviews && <p>Loading reviews...</p>}
                    {reviewError && <p className="error-text">{reviewError}</p>}
                    {!loadingReviews && !reviewError && restaurantReviews.length === 0 && (
                      <p>No reviews found for this restaurant.</p>
                    )}
                    {!loadingReviews && !reviewError && restaurantReviews.length > 0 && (
                      <ul className="review-list">
                        {restaurantReviews.map((review) => (
                          <li key={review.review_id} className="review-item">
                            <strong>{review.reviewer_name || review.user_id || 'Anonymous'}:</strong> {review.rating ? `⭐${review.rating}` : ''}<br />
                            <span>{review.comment || review.review_text || ''}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </section>
                )}
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
                      <button type="button" onClick={() => handleSelectRestaurant(restaurant.restaurant_id)}>
                        View menu
                      </button>
                    </article>
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
