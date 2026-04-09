
import { useEffect, useState } from 'react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const AUTH_STORAGE_KEY = 'goat-food-auth';

function formatMoney(value) {
  const number = Number(value);
  return Number.isNaN(number) ? '-' : number.toFixed(2);
}


function getRestaurantDisplayName(order, restaurants) {
  return (
    order.restaurant_name ||
    restaurants.find((restaurant) => String(restaurant.restaurant_id) === String(order.restaurant_id))?.restaurant_name ||
    order.restaurant_id
  );
}

function getFoodItemDisplayName(item, foodItems) {
  return (
    item.food_item_name ||
    item.food_name ||
    foodItems.find((food) => String(food.food_item_id) === String(item.food_item_id))?.food_name ||
    `Item #${item.food_item_id}`
  );
}

function isAuthMissingUserError(error) {
  return typeof error?.message === 'string' && /404/.test(error.message);
}

function App() {
      // Submit review handler
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
    // Review form handlers
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
  // State for review forms
  const [reviewForms, setReviewForms] = useState({});
  // Helper to check if an order can be reviewed (must be after auth is defined)
  const canReviewOrder = (order) => {
    // Only allow review if order is completed and user is a customer
    return auth?.role === 'CUSTOMER' && order.status === 'COMPLETED';
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
  const [favorites, setFavorites] = useState([]);
  const [loadingFavorites, setLoadingFavorites] = useState(false);
  const [favoritesError, setFavoritesError] = useState('');
  const [orders, setOrders] = useState([]);
  const [loadingOrders, setLoadingOrders] = useState(false);
  const [ordersError, setOrdersError] = useState('');
  const [orderFilterRestaurant, setOrderFilterRestaurant] = useState('');
  const [orderFilterCuisine, setOrderFilterCuisine] = useState('');
  const [orderFilterAccepted, setOrderFilterAccepted] = useState('all');
  const [orderFilterDate, setOrderFilterDate] = useState('');
  const [orderSortBy, setOrderSortBy] = useState('date');
  const [orderSortOrder, setOrderSortOrder] = useState('desc');
  const [inventory, setInventory] = useState({});
  const [inventoryDrafts, setInventoryDrafts] = useState({});
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
  const [newFoodInventoryQuantity, setNewFoodInventoryQuantity] = useState('');
  const [foodStats, setFoodStats] = useState([]);
  const [loadingFoodStats, setLoadingFoodStats] = useState(true);
  const [foodStatsError, setFoodStatsError] = useState("");
  const [newRestaurantName, setNewRestaurantName] = useState('');
  const [newRestaurantCuisine, setNewRestaurantCuisine] = useState('');
  const [newRestaurantAddress, setNewRestaurantAddress] = useState('');
  const [newRestaurantOpenHour, setNewRestaurantOpenHour] = useState('09:00');
  const [newRestaurantClosedHour, setNewRestaurantClosedHour] = useState('21:00');
  const [restaurantCreateError, setRestaurantCreateError] = useState('');
  const [restaurantCreateMessage, setRestaurantCreateMessage] = useState('');
  const [loadingPastOrders, setLoadingPastOrders] = useState(false);
  const [pastOrders, setPastOrders] = useState([]);
  const [staffAssignments, setStaffAssignments] = useState([]);
  const [loadingStaffAssignments, setLoadingStaffAssignments] = useState(false);
  const [staffAssignmentError, setStaffAssignmentError] = useState('');
  const [selectedStaffRestaurantId, setSelectedStaffRestaurantId] = useState('');
  const [restaurantOrders, setRestaurantOrders] = useState([]);
  const [loadingRestaurantOrders, setLoadingRestaurantOrders] = useState(false);
  const [restaurantOrderError, setRestaurantOrderError] = useState('');
  const [restaurantCourierAssignments, setRestaurantCourierAssignments] = useState([]);
  const [selectedCourierByOrder, setSelectedCourierByOrder] = useState({});
  const [courierOrders, setCourierOrders] = useState([]);
  const [loadingCourierOrders, setLoadingCourierOrders] = useState(false);
  const [courierOrderError, setCourierOrderError] = useState('');
  const [orderActionMessage, setOrderActionMessage] = useState('');
  const [orderActionError, setOrderActionError] = useState('');
  const [loadingMostOrdered, setLoadingMostOrdered] = useState(false);
  const [mostOrderedError, setMostOrderedError] = useState(null);
  const [mostOrdered, setMostOrdered] = useState([]);
  const [restaurantStaffAssignments, setRestaurantStaffAssignments] = useState([]);
  const [loadingRestaurantStaffAssignments, setLoadingRestaurantStaffAssignments] = useState(false);
  const [restaurantStaffAssignmentError, setRestaurantStaffAssignmentError] = useState('');
  const [restaurantId, setRestaurantId] = useState(null);
  const [staffAssignmentMessage, setStaffAssignmentMessage] = useState('');
  const [staffAssignmentFormEmail, setStaffAssignmentFormEmail] = useState('');
  const [staffAssignmentFormRole, setStaffAssignmentFormRole] = useState('MANAGER');
  const [staffDirectory, setStaffDirectory] = useState({});
  const [auth, setAuth] = useState(null);
  const [selectedRestaurantId, setSelectedRestaurantId] = useState(null);
  const selectedRestaurant = restaurants.find((restaurant) => String(restaurant.restaurant_id) === String(selectedRestaurantId)) || null;
  const restaurantFoodItems = selectedRestaurant
    ? foodItems.filter((item) => String(item.restaurant_id) === String(selectedRestaurant.restaurant_id))
    : foodItems;
  const staffAssignedRestaurantIds = new Set(staffAssignments.map((assignment) => String(assignment.restaurant_id)));
  const staffAccessibleRestaurants = auth?.role === 'STAFF'
    ? restaurants.filter(
        (restaurant) =>
          String(restaurant.owner_id) === String(auth?.user_id) ||
          staffAssignedRestaurantIds.has(String(restaurant.restaurant_id))
      )
    : [];
  const activeStaffRestaurantId = staffAccessibleRestaurants.some(
    (restaurant) => String(restaurant.restaurant_id) === String(selectedStaffRestaurantId)
  )
    ? String(selectedStaffRestaurantId)
    : (staffAccessibleRestaurants[0] ? String(staffAccessibleRestaurants[0].restaurant_id) : '');
  const activeStaffRestaurant = staffAccessibleRestaurants.find(
    (restaurant) => String(restaurant.restaurant_id) === activeStaffRestaurantId
  ) || null;
  const managedInventoryItems = activeStaffRestaurantId
    ? foodItems.filter((item) => String(item.restaurant_id) === activeStaffRestaurantId)
    : [];
  const managedFoodItems = activeStaffRestaurantId
    ? foodItemsManagement.filter((item) => String(item.restaurant_id) === activeStaffRestaurantId)
    : [];
  const ownerRestaurant = auth?.role === 'STAFF'
    ? staffAccessibleRestaurants.find((restaurant) => String(restaurant.owner_id) === String(auth?.user_id)) || null
    : null;
  const currentAssignmentRoles = Array.from(new Set(staffAssignments.map((assignment) => assignment.assignment)));
  const canManageRestaurant = currentAssignmentRoles.includes('OWNER') || currentAssignmentRoles.includes('MANAGER');
  const isCourierOnly = currentAssignmentRoles.includes('COURIER') && !canManageRestaurant;
  // Removed showProfilePage state, profile always shown inline now
  // Reviews state
  const [restaurantReviews, setRestaurantReviews] = useState([]);
  const [loadingReviews, setLoadingReviews] = useState(false);
  const [reviewError, setReviewError] = useState('');
    // Fetch reviews when a restaurant is selected
  useEffect(() => {
    if (auth?.role !== 'STAFF') {
      return;
    }
    if (staffAccessibleRestaurants.length === 0) {
      if (selectedStaffRestaurantId) {
        setSelectedStaffRestaurantId('');
      }
      return;
    }
    if (!staffAccessibleRestaurants.some((restaurant) => String(restaurant.restaurant_id) === String(selectedStaffRestaurantId))) {
      setSelectedStaffRestaurantId(String(staffAccessibleRestaurants[0].restaurant_id));
    }
  }, [auth?.role, selectedStaffRestaurantId, staffAccessibleRestaurants]);

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
          // If 404, show a friendly message
          if (err.message && err.message.includes('404')) {
            setReviewError('no reviews yet');
          } else {
            setReviewError(`Unable to load reviews. ${err.message}`);
          }
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

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }
    const saved = localStorage.getItem(AUTH_STORAGE_KEY);
    if (saved) {
      setAuth(JSON.parse(saved));
    }
  }, []);

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
  const fetchMostOrdered = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/stat/restaurant/stats"
      );

      setMostOrdered(response.data);

      const validRestaurants = response.data.filter(
        (r) =>
          typeof r.restaurant_name === "string" &&
          r.restaurant_name.trim() !== ""
      );

      if (validRestaurants.length > 0) {
        setRestaurantId(validRestaurants[0].restaurant_id);
      }

      setLoadingMostOrdered(false);
    } catch (err) {
      console.error(err);
      setMostOrderedError("Failed to load most ordered restaurants");
      setLoadingMostOrdered(false);
    }
  };

  if (auth) {
    fetchMostOrdered();
  }
}, [auth]);

useEffect(() => {
  const fetchFoodStats = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/food_stat/food_items/${restaurantId}/stats`
      );

      setFoodStats(response.data);
      setLoadingFoodStats(false);
    } catch (err) {
      console.error(err);
      setFoodStatsError("Failed to load food stats");
      setLoadingFoodStats(false);
    }
  };

  if (auth && restaurantId) {
    fetchFoodStats();
  }
}, [auth, restaurantId]);

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
      loadUserProfile(auth.user_id);
      if (auth.role === 'CUSTOMER') {
        loadPastOrders(auth.user_id);
      }
      if (auth.role === 'STAFF') {
        loadStaffAssignments(auth.user_id);
      }
      loadFavorites();
      if (auth.role === 'STAFF') {
        loadFoodItemsManagement();
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

  const loadRestaurantCourierAssignments = async (restaurantId) => {
    if (!auth?.token || !restaurantId) {
      setRestaurantCourierAssignments([]);
      return;
    }
    try {
      const response = await fetch(`${API_BASE_URL}/staff-assignments/restaurant/${encodeURIComponent(restaurantId)}`, {
        headers: authHeaders(),
      });
      if (!response.ok) {
        throw new Error(`Unable to load couriers (${response.status})`);
      }
      const data = await response.json();
      const assignments = Array.isArray(data) ? data : [];
      setRestaurantCourierAssignments(assignments.filter((assignment) => assignment.assignment === 'COURIER'));
    } catch (err) {
      setRestaurantCourierAssignments([]);
      setOrderActionError(err.message);
    }
  };

  const loadCourierOrders = async () => {
    if (!auth?.token) {
      setCourierOrders([]);
      return;
    }
    setLoadingCourierOrders(true);
    setCourierOrderError('');

    try {
      const response = await fetch(`${API_BASE_URL}/deliveries/my-orders`, {
        headers: authHeaders(),
      });
      if (!response.ok) {
        throw new Error(`Unable to load courier orders (${response.status})`);
      }
      const data = await response.json();
      setCourierOrders(Array.isArray(data) ? data : []);
    } catch (err) {
      setCourierOrderError(err.message);
      setCourierOrders([]);
    } finally {
      setLoadingCourierOrders(false);
    }
  };

  const loadRestaurantStaffAssignments = async (restaurantId) => {
    if (!auth?.token || !restaurantId) {
      setRestaurantStaffAssignments([]);
      return;
    }
    setLoadingRestaurantStaffAssignments(true);
    setRestaurantStaffAssignmentError('');

    try {
      const response = await fetch(`${API_BASE_URL}/staff-assignments/restaurant/${encodeURIComponent(restaurantId)}`, {
        headers: authHeaders(),
      });
      if (!response.ok) {
        throw new Error(`Unable to load restaurant staff (${response.status})`);
      }
      const data = await response.json();
      setRestaurantStaffAssignments(Array.isArray(data) ? data : []);
    } catch (err) {
      setRestaurantStaffAssignmentError(err.message);
      setRestaurantStaffAssignments([]);
    } finally {
      setLoadingRestaurantStaffAssignments(false);
    }
  };

  useEffect(() => {
    if (auth?.role === 'STAFF' && selectedStaffRestaurantId) {
      loadRestaurantOrders(selectedStaffRestaurantId);
      loadRestaurantCourierAssignments(selectedStaffRestaurantId);
    } else {
      setRestaurantOrders([]);
      setRestaurantCourierAssignments([]);
    }
  }, [selectedStaffRestaurantId, auth]);

  useEffect(() => {
    if (auth?.role !== 'STAFF') {
      return;
    }
    if (!activeStaffRestaurantId) {
      setNewFoodRestaurantId('');
      return;
    }
    setNewFoodRestaurantId(activeStaffRestaurantId);
  }, [auth?.role, activeStaffRestaurantId]);

  useEffect(() => {
    if (auth?.role === 'STAFF' && isCourierOnly) {
      loadCourierOrders();
    } else {
      setCourierOrders([]);
    }
  }, [auth?.role, auth?.token, isCourierOnly]);

  useEffect(() => {
    if (auth?.role === 'CUSTOMER' && auth?.user_id) {
      loadPastOrders(auth.user_id);
    }
  }, [
    auth?.role,
    auth?.user_id,
    orderFilterRestaurant,
    orderFilterCuisine,
    orderFilterAccepted,
    orderFilterDate,
    orderSortBy,
    orderSortOrder,
  ]);

  useEffect(() => {
    if (ownerRestaurant?.restaurant_id) {
      loadRestaurantStaffAssignments(ownerRestaurant.restaurant_id);
    } else {
      setRestaurantStaffAssignments([]);
    }
  }, [ownerRestaurant?.restaurant_id, auth?.token]);

  useEffect(() => {
    const staffIds = Array.from(
      new Set(
        [...staffAssignments, ...restaurantStaffAssignments]
          .map((assignment) => assignment?.staff_id)
          .filter(Boolean)
      )
    ).filter((staffId) => !staffDirectory[staffId]);

    if (staffIds.length === 0) {
      return;
    }

    Promise.all(
      staffIds.map(async (staffId) => {
        const response = await fetch(`${API_BASE_URL}/users/${encodeURIComponent(staffId)}`);
        if (!response.ok) {
          return [staffId, null];
        }
        const data = await response.json();
        return [staffId, data];
      })
    ).then((entries) => {
      setStaffDirectory((prev) => {
        const next = { ...prev };
        for (const [staffId, data] of entries) {
          next[staffId] = data;
        }
        return next;
      });
    });
  }, [staffAssignments, restaurantStaffAssignments, staffDirectory]);

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

  const handleAssignCourierToOrder = async (order) => {
    if (!auth?.token) {
      setOrderActionError('Please log in to assign a courier.');
      return;
    }
    const courierId = selectedCourierByOrder[order.order_id];
    if (!courierId) {
      setOrderActionError('Choose a courier first.');
      return;
    }
    if (!order.delivery_id) {
      setOrderActionError('This order does not have a delivery record yet. Accept it first.');
      return;
    }

    setOrderActionMessage('');
    setOrderActionError('');

    try {
      const response = await fetch(`${API_BASE_URL}/deliveries/assign/${encodeURIComponent(order.delivery_id)}/${encodeURIComponent(courierId)}`, {
        method: 'PUT',
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Assign courier failed (${response.status}) ${body}`);
      }

      setOrderActionMessage('Courier assigned successfully.');
      await loadRestaurantOrders(selectedStaffRestaurantId);
    } catch (err) {
      setOrderActionError(err.message);
    }
  };

  const handlePickupDelivery = async (deliveryId) => {
    if (!deliveryId) {
      setCourierOrderError('This order does not have a delivery assigned.');
      return;
    }
    try {
      const response = await fetch(`${API_BASE_URL}/deliveries/pickup/${encodeURIComponent(deliveryId)}`, {
        method: 'PUT',
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Update failed (${response.status}) ${body}`);
      }
      await loadCourierOrders();
    } catch (err) {
      setCourierOrderError(err.message);
    }
  };

  const handleCompleteDelivery = async (deliveryId) => {
    if (!deliveryId) {
      setCourierOrderError('This order does not have a delivery assigned.');
      return;
    }
    try {
      const response = await fetch(`${API_BASE_URL}/deliveries/complete/${encodeURIComponent(deliveryId)}`, {
        method: 'PUT',
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Update failed (${response.status}) ${body}`);
      }
      await loadCourierOrders();
    } catch (err) {
      setCourierOrderError(err.message);
    }
  };

  const authHeaders = () => ({
    token: auth?.token || '',
    'Content-Type': 'application/json',
  });

  const resolveStaffUserByEmail = async (email) => {
    const response = await fetch(`${API_BASE_URL}/users/by-email/${encodeURIComponent(email)}`);
    if (!response.ok) {
      throw new Error(`Unable to find staff user (${response.status})`);
    }
    return response.json();
  };

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

  const handleCancelOrderCustomer = async (orderId) => {
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
      // Reload the appropriate order list based on user role
      if (auth?.role === 'CUSTOMER') {
        await loadPastOrders(auth.user_id);
      } else {
        await loadRestaurantOrders(selectedStaffRestaurantId);
      }
    } catch (err) {
      setOrdersError(err.message);
    }
  };

  const handleAcceptOrderHistory = async (orderId) => {
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
      await loadPastOrders(auth.user_id);
    } catch (err) {
      setOrdersError(err.message);
    }
  };

  const handleCancelOrderStaffHistory = async (orderId) => {
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
      await loadPastOrders(auth.user_id);
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
          setInventoryDrafts((prev) => ({ ...prev, [foodItemId]: '' }));
          return;
        }
        throw new Error(`Unable to load inventory (${response.status})`);
      }
      const data = await response.json();
      setInventory((prev) => ({ ...prev, [foodItemId]: data }));
      setInventoryDrafts((prev) => ({ ...prev, [foodItemId]: String(data.quantity ?? '') }));
    } catch (err) {
      setInventoryError(err.message);
      setInventory((prev) => ({ ...prev, [foodItemId]: null }));
      setInventoryDrafts((prev) => ({ ...prev, [foodItemId]: '' }));
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
      // First try to update existing inventory
      let response = await fetch(`${API_BASE_URL}/inventory/${encodeURIComponent(foodItemId)}`, {
        method: 'PATCH',
        headers: authHeaders(),
        body: JSON.stringify({ quantity: newQuantity }),
      });

      if (response.status === 404) {
        // If inventory doesn't exist, create it
        response = await fetch(`${API_BASE_URL}/inventory/`, {
          method: 'POST',
          headers: authHeaders(),
          body: JSON.stringify({ food_item_id: foodItemId, quantity: newQuantity }),
        });
      }

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Update inventory failed (${response.status}) ${body}`);
      }
      const updatedInventory = await response.json();
      setInventory((prev) => ({ ...prev, [foodItemId]: updatedInventory }));
      setInventoryDrafts((prev) => ({ ...prev, [foodItemId]: String(updatedInventory.quantity ?? '') }));
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

  const handleAssignStaffMember = async (event) => {
    event.preventDefault();
    if (!auth?.token) {
      setRestaurantStaffAssignmentError('Please log in to manage staff assignments.');
      return;
    }
    setRestaurantStaffAssignmentError('');
    setStaffAssignmentMessage('');

    try {
      const staffUser = await resolveStaffUserByEmail(staffAssignmentFormEmail.trim());
      const response = await fetch(`${API_BASE_URL}/staff-assignments/assign_staff`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({
          staff_id: staffUser.id,
          assignment: staffAssignmentFormRole,
        }),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Assign staff failed (${response.status}) ${body}`);
      }

      setStaffAssignmentFormEmail('');
      setStaffAssignmentFormRole('MANAGER');
      setStaffAssignmentMessage(`Assigned ${staffUser.email} as ${staffAssignmentFormRole}.`);
      await loadRestaurantStaffAssignments(ownerRestaurant?.restaurant_id);
      await loadStaffAssignments(auth.user_id);
    } catch (err) {
      setRestaurantStaffAssignmentError(err.message);
    }
  };

  const handleUpdateStaffAssignmentRole = async (staffId, assignment) => {
    if (!auth?.token) {
      setRestaurantStaffAssignmentError('Please log in to manage staff assignments.');
      return;
    }
    setRestaurantStaffAssignmentError('');
    setStaffAssignmentMessage('');

    try {
      const response = await fetch(`${API_BASE_URL}/staff-assignments/update_staff/${encodeURIComponent(staffId)}`, {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify({ assignment }),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Update assignment failed (${response.status}) ${body}`);
      }

      setStaffAssignmentMessage(`Updated role to ${assignment}.`);
      await loadRestaurantStaffAssignments(ownerRestaurant?.restaurant_id);
      await loadStaffAssignments(auth.user_id);
    } catch (err) {
      setRestaurantStaffAssignmentError(err.message);
    }
  };

  const handleRemoveStaffAssignment = async (staffId) => {
    if (!auth?.token) {
      setRestaurantStaffAssignmentError('Please log in to manage staff assignments.');
      return;
    }
    setRestaurantStaffAssignmentError('');
    setStaffAssignmentMessage('');

    try {
      const response = await fetch(`${API_BASE_URL}/staff-assignments/remove_staff/${encodeURIComponent(staffId)}`, {
        method: 'DELETE',
        headers: authHeaders(),
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Remove assignment failed (${response.status}) ${body}`);
      }

      setStaffAssignmentMessage('Staff assignment removed.');
      await loadRestaurantStaffAssignments(ownerRestaurant?.restaurant_id);
      await loadStaffAssignments(auth.user_id);
    } catch (err) {
      setRestaurantStaffAssignmentError(err.message);
    }
  };

  const renderStaffAssignmentManager = () => {
    if (!ownerRestaurant) {
      return null;
    }

    return (
      <div className="restaurant-order-management-card">
        <h4>Manage Staff Assignments</h4>
        <p><strong>Owner restaurant:</strong> {ownerRestaurant.restaurant_name} ({ownerRestaurant.restaurant_id})</p>
        {staffAssignmentMessage && <p className="success-text">{staffAssignmentMessage}</p>}
        {restaurantStaffAssignmentError && <p className="error-text">{restaurantStaffAssignmentError}</p>}

        <form className="food-form" onSubmit={handleAssignStaffMember}>
          <div className="form-grid">
            <label>
              Staff email
              <input
                type="email"
                value={staffAssignmentFormEmail}
                onChange={(event) => setStaffAssignmentFormEmail(event.target.value)}
                placeholder="staff@example.com"
                required
              />
            </label>
            <label>
              Assignment role
              <select
                value={staffAssignmentFormRole}
                onChange={(event) => setStaffAssignmentFormRole(event.target.value)}
                required
              >
                <option value="MANAGER">MANAGER</option>
                <option value="COURIER">COURIER</option>
              </select>
            </label>
          </div>
          <div className="form-actions">
            <button type="submit">Assign Staff</button>
          </div>
        </form>

        {loadingRestaurantStaffAssignments && <p>Loading restaurant staff...</p>}
        {!loadingRestaurantStaffAssignments && restaurantStaffAssignments.length === 0 && (
          <p>No staff assignments found for this restaurant yet.</p>
        )}
        {!loadingRestaurantStaffAssignments && restaurantStaffAssignments.length > 0 && (
          <div className="staff-assignment-list">
            {restaurantStaffAssignments.map((assignment) => (
              <article key={`${assignment.restaurant_id}-${assignment.staff_id}`} className="assignment-card">
                <p><strong>Name:</strong> {staffDirectory[assignment.staff_id]?.first_name ?? 'Unknown'} {staffDirectory[assignment.staff_id]?.last_name ?? ''}</p>
                <p><strong>Staff ID:</strong> {assignment.staff_id}</p>
                <p><strong>Assignment ID:</strong> {assignment.assignment_id}</p>
                <p><strong>Current Role:</strong> {assignment.assignment}</p>
                {assignment.staff_id !== auth?.user_id && (
                  <>
                    <label>
                      Change role
                      <select
                        value={assignment.assignment}
                        onChange={(event) => handleUpdateStaffAssignmentRole(assignment.staff_id, event.target.value)}
                      >
                        <option value="MANAGER">MANAGER</option>
                        <option value="COURIER">COURIER</option>
                      </select>
                    </label>
                    <button
                      type="button"
                      className="danger"
                      onClick={() => handleRemoveStaffAssignment(assignment.staff_id)}
                    >
                      Remove Assignment
                    </button>
                  </>
                )}
              </article>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderRestaurantOrderManager = () => (
    <div className="restaurant-order-management-card">
      <h4>Incoming Restaurant Orders</h4>
      {activeStaffRestaurant && (
        <p><strong>Restaurant:</strong> {activeStaffRestaurant.restaurant_name} ({activeStaffRestaurant.restaurant_id})</p>
      )}

      {orderActionMessage && <p className="success-text">{orderActionMessage}</p>}
      {orderActionError && <p className="error-text">{orderActionError}</p>}
      {loadingRestaurantOrders && <p>Loading restaurant orders...</p>}
      {restaurantOrderError && <p className="error-text">{restaurantOrderError}</p>}
      {!loadingRestaurantOrders && !restaurantOrderError && restaurantOrders.length === 0 && (
        <p>No orders found for this restaurant.</p>
      )}
      {!loadingRestaurantOrders && restaurantOrders.length > 0 && (
        <div className="order-history-list">
          {restaurantOrders.map((order) => {
            const assignedCourier = restaurantCourierAssignments.find(
              (assignment) => assignment.staff_id === selectedCourierByOrder[order.order_id]
            );
            return (
              <article key={order.order_id} className="order-card">
                <p><strong>Order #</strong> {order.order_id}</p>
                <p><strong>Status:</strong> {order.status}</p>
                <p><strong>Placed:</strong> {new Date(order.created_date).toLocaleString()}</p>
                <p><strong>Total:</strong> ${formatMoney(order.total_amount)}</p>
                <p><strong>Customer:</strong> {order.customer_id}</p>
                <p><strong>Delivery address:</strong> {order.delivery_address || order.delivery_address_id}</p>
                <p><strong>Delivery ID:</strong> {order.delivery_id || 'Not created yet'}</p>
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
                {order.status === 'PENDING' && canManageRestaurant && (
                  <div className="order-action-buttons">
                    <button type="button" onClick={() => handleAcceptOrder(order.order_id)}>
                      Accept Order
                    </button>
                    <button type="button" className="danger" onClick={() => handleCancelOrderRestaurant(order.order_id)}>
                      Cancel
                    </button>
                  </div>
                )}
                {order.status === 'ACCEPTED' && (
                  <div className="order-action-buttons">
                    <label>
                      Assign courier
                      <select
                        value={selectedCourierByOrder[order.order_id] ?? ''}
                        onChange={(event) =>
                          setSelectedCourierByOrder((prev) => ({ ...prev, [order.order_id]: event.target.value }))
                        }
                      >
                        <option value="">Select courier</option>
                        {restaurantCourierAssignments.map((assignment) => (
                          <option key={`${order.order_id}-${assignment.staff_id}`} value={assignment.staff_id}>
                            {staffDirectory[assignment.staff_id]?.first_name ?? assignment.staff_id}
                            {staffDirectory[assignment.staff_id]?.last_name ? ` ${staffDirectory[assignment.staff_id].last_name}` : ''}
                          </option>
                        ))}
                      </select>
                    </label>
                    <button type="button" onClick={() => handleAssignCourierToOrder(order)}>
                      Assign Courier
                    </button>
                    <button type="button" className="danger" onClick={() => handleCancelOrderRestaurant(order.order_id)}>
                      Cancel
                    </button>
                    {assignedCourier && (
                      <p><strong>Selected Courier:</strong> {staffDirectory[assignedCourier.staff_id]?.first_name ?? assignedCourier.staff_id} {staffDirectory[assignedCourier.staff_id]?.last_name ?? ''}</p>
                    )}
                  </div>
                )}
              </article>
            );
          })}
        </div>
      )}
    </div>
  );

  const renderCourierOrderManager = () => (
    <div className="restaurant-order-management-card">
      <h4>Assigned Deliveries</h4>
      {courierOrderError && <p className="error-text">{courierOrderError}</p>}
      {loadingCourierOrders && <p>Loading assigned deliveries...</p>}
      {!loadingCourierOrders && courierOrders.length === 0 && (
        <p>No deliveries have been assigned to you yet.</p>
      )}
      {!loadingCourierOrders && courierOrders.length > 0 && (
        <div className="order-history-list">
          {courierOrders.map((order) => (
            <article key={order.order_id} className="order-card">
              <p><strong>Order #</strong> {order.order_id}</p>
              <p><strong>Status:</strong> {order.status}</p>
              <p><strong>Placed:</strong> {new Date(order.created_date).toLocaleString()}</p>
              <p><strong>Total:</strong> ${formatMoney(order.total_amount)}</p>
              <p><strong>Delivery address:</strong> {order.delivery_address || order.delivery_address_id}</p>
              <p><strong>Delivery ID:</strong> {order.delivery_id || 'Missing'}</p>
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
              <div className="order-action-buttons">
                {order.status === 'ACCEPTED' && (
                  <button type="button" onClick={() => handlePickupDelivery(order.delivery_id)}>
                    Mark Out for Delivery
                  </button>
                )}
                {order.status === 'OUT_FOR_DELIVERY' && (
                  <button type="button" onClick={() => handleCompleteDelivery(order.delivery_id)}>
                    Mark Delivered
                  </button>
                )}
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );

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

  const handleCreateRestaurant = async (event) => {
    event.preventDefault();
    if (!auth?.token) {
      setRestaurantCreateError('Please log in to create a restaurant.');
      return;
    }

    setRestaurantCreateError('');
    setRestaurantCreateMessage('');

    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({
          restaurant_name: newRestaurantName,
          cuisine: newRestaurantCuisine,
          address: newRestaurantAddress,
          open_hour: newRestaurantOpenHour,
          closed_hour: newRestaurantClosedHour,
        }),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`Create restaurant failed (${response.status}) ${body}`);
      }

      const createdRestaurant = await response.json();
      setRestaurants((prev) => [...prev, createdRestaurant]);
      setSelectedStaffRestaurantId(String(createdRestaurant.restaurant_id));
      setNewFoodRestaurantId(String(createdRestaurant.restaurant_id));
      setRestaurantCreateMessage(`Restaurant ${createdRestaurant.restaurant_name} created successfully.`);
      setNewRestaurantName('');
      setNewRestaurantCuisine('');
      setNewRestaurantAddress('');
      setNewRestaurantOpenHour('09:00');
      setNewRestaurantClosedHour('21:00');
      await loadStaffAssignments(auth.user_id);
    } catch (err) {
      setRestaurantCreateError(err.message);
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

      // Update inventory quantity
      if (newFoodInventoryQuantity !== '') {
        try {
          // First try to update existing inventory
          let inventoryResponse = await fetch(`${API_BASE_URL}/inventory/${encodeURIComponent(editingFoodItem.food_item_id)}`, {
            method: 'PATCH',
            headers: authHeaders(),
            body: JSON.stringify({ quantity: parseInt(newFoodInventoryQuantity) }),
          });

          if (inventoryResponse.status === 404) {
            // If inventory doesn't exist, create it
            inventoryResponse = await fetch(`${API_BASE_URL}/inventory/`, {
              method: 'POST',
              headers: authHeaders(),
              body: JSON.stringify({ food_item_id: editingFoodItem.food_item_id, quantity: parseInt(newFoodInventoryQuantity) }),
            });
          }

          if (inventoryResponse.ok) {
            const updatedInventory = await inventoryResponse.json();
            setInventory((prev) => ({ ...prev, [editingFoodItem.food_item_id]: updatedInventory }));
          } else {
            const body = await inventoryResponse.text();
            console.warn(`Inventory update failed (${inventoryResponse.status}): ${body}`);
          }
        } catch (inventoryErr) {
          console.warn('Failed to update inventory:', inventoryErr);
        }
      }

      // Reset form
      setEditingFoodItem(null);
      setNewFoodName('');
      setNewFoodPrice('');
      setNewFoodDescription('');
      setNewFoodCourse('');
      setNewFoodInventoryQuantity('');
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

  const handleEditFoodItem = async (foodItem) => {
    setEditingFoodItem(foodItem);
    setNewFoodName(foodItem.food_name);
    setNewFoodPrice(foodItem.price.toString());
    setNewFoodDescription(foodItem.description);
    setNewFoodCourse(foodItem.course);

    // Load inventory quantity for this food item
    try {
      const response = await fetch(`${API_BASE_URL}/inventory/${foodItem.food_item_id}`, {
        headers: authHeaders(),
      });
      if (response.ok) {
        const inventoryData = await response.json();
        setNewFoodInventoryQuantity(inventoryData.quantity.toString());
      } else {
        setNewFoodInventoryQuantity('0');
      }
    } catch (err) {
      console.warn('Failed to load inventory for editing:', err);
      setNewFoodInventoryQuantity('0');
    }
  };

  const handleCancelEdit = () => {
    setEditingFoodItem(null);
    setNewFoodName('');
    setNewFoodPrice('');
    setNewFoodDescription('');
    setNewFoodCourse('');
    setNewFoodInventoryQuantity('');
  };

  const handleSelectRestaurant = (restaurantId) => {
    setSelectedRestaurantId(restaurantId);
  };

  const handleClearSelectedRestaurant = () => {
    setSelectedRestaurantId(null);
  };

  // Removed handleOpenProfile and handleCloseProfile

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
      if (isAuthMissingUserError(err)) {
        localStorage.removeItem(AUTH_STORAGE_KEY);
        setAuth(null);
        setProfileError('Your saved session no longer matches a user in this backend. Please log in again.');
        return;
      }
      setProfileError(`Unable to load profile. ${err.message}`);
    } finally {
      setLoadingProfile(false);
    }
  };

  const loadPastOrders = async (userId) => {
    if (!userId) return;
    setLoadingPastOrders(true);
    setProfileError('');
    setLoadingOrders(true);
    setOrdersError('');

    try {
      let data;
      const params = new URLSearchParams();
      if (orderFilterRestaurant.trim()) {
        params.set('restaurant', orderFilterRestaurant.trim());
      }
      if (orderFilterCuisine.trim()) {
        params.set('cuisine', orderFilterCuisine.trim());
      }
      if (orderFilterAccepted !== 'all') {
        params.set('accepted', orderFilterAccepted);
      }
      if (orderFilterDate) {
        params.set('date', orderFilterDate);
      }
      params.set('sort_by', orderSortBy);
      params.set('sort_order', orderSortOrder);

      const historyResponse = await fetch(`${API_BASE_URL}/orders/order_history?${params.toString()}`, {
        headers: authHeaders(),
      });

      if (historyResponse.ok) {
        data = await historyResponse.json();
      } else if (!params.toString()) {
        const fallbackResponse = await fetch(`${API_BASE_URL}/orders/get_order_by_user/${encodeURIComponent(userId)}`, {
          headers: authHeaders(),
        });
        if (!fallbackResponse.ok) {
          throw new Error(`Unable to load orders (${fallbackResponse.status})`);
        }
        data = await fallbackResponse.json();
      }

      const normalizedOrders = Array.isArray(data) ? data : [];
      setPastOrders(normalizedOrders);
      setOrders(normalizedOrders);
    } catch (err) {
      setProfileError(`Unable to load order history. ${err.message}`);
      setPastOrders([]);
      setOrders([]);
      setOrdersError(`Unable to load orders. ${err.message}`);
    } finally {
      setLoadingPastOrders(false);
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
      localStorage.removeItem(AUTH_STORAGE_KEY);
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
        await loadPastOrders(auth.user_id);
      }
    } catch (err) {
      // Custom message for payment not processed
      if (typeof err.message === 'string' && err.message.includes('payment not processed order')) {
        setOrderError('Payment failed, try again');
      } else {
        setOrderError(err.message);
      }
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
    setOrderSuccess(''); // Clear order success message when cart is updated
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
        // If staff user and cart not found (404), show custom message
        if (response.status === 404 && auth?.role === 'STAFF') {
          setCartError('Only customers can add items to cart.');
          return;
        }
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

        {/* Profile section always visible when logged in */}
        {auth && (
          <section className="card profile-card">
            <div className="profile-header-row">
              <h2>My Profile</h2>
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
          </section>
        )}
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
                            <span>{review.review || review.comment || review.review_text || ''}</span>
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
                  {auth?.role === 'CUSTOMER' && order.status === 'PENDING' && (
                    <div className="order-action-buttons">
                      <button type="button" className="danger" onClick={() => handleCancelOrderCustomer(order.order_id)}>
                        Cancel Order
                      </button>
                    </div>
                  )}
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
          {auth?.role === 'CUSTOMER' && (
            <div className="form-grid">
              <label>
                Restaurant
                <input
                  type="text"
                  value={orderFilterRestaurant}
                  onChange={(event) => setOrderFilterRestaurant(event.target.value)}
                  placeholder="Filter by restaurant"
                />
              </label>
              <label>
                Cuisine
                <input
                  type="text"
                  value={orderFilterCuisine}
                  onChange={(event) => setOrderFilterCuisine(event.target.value)}
                  placeholder="Filter by cuisine"
                />
              </label>
              <label>
                Accepted
                <select
                  value={orderFilterAccepted}
                  onChange={(event) => setOrderFilterAccepted(event.target.value)}
                >
                  <option value="all">All</option>
                  <option value="true">Accepted only</option>
                  <option value="false">Not accepted</option>
                </select>
              </label>
              <label>
                Date
                <input
                  type="date"
                  value={orderFilterDate}
                  onChange={(event) => setOrderFilterDate(event.target.value)}
                />
              </label>
              <label>
                Sort by
                <select
                  value={orderSortBy}
                  onChange={(event) => setOrderSortBy(event.target.value)}
                >
                  <option value="date">Date</option>
                  <option value="restaurant">Restaurant</option>
                  <option value="cuisine">Cuisine</option>
                </select>
              </label>
              <label>
                Sort order
                <select
                  value={orderSortOrder}
                  onChange={(event) => setOrderSortOrder(event.target.value)}
                >
                  <option value="desc">Newest first</option>
                  <option value="asc">Oldest first</option>
                </select>
              </label>
            </div>
          )}
          {auth && loadingOrders && <p>Loading orders...</p>}
          {auth && ordersError && <p className="error-text">{ordersError}</p>}
          {auth && !loadingOrders && orders.length === 0 && (
            <p>You have no orders yet. Add items to your cart and submit an order to get started.</p>
          )}
          {auth && !loadingOrders && orders.length > 0 && (
            <div className="order-history-list">
              {pastOrders.map((order) => (
                <article key={order.order_id} className="order-card">
                  <p><strong>Order #</strong> {order.order_id}</p>
                  <p><strong>Status:</strong> {order.status}</p>
                  <p><strong>Placed:</strong> {new Date(order.created_date).toLocaleString()}</p>
                  <p><strong>Total:</strong> ${formatMoney(order.total_amount)}</p>
                  <p><strong>Restaurant:</strong> {getRestaurantDisplayName(order, restaurants)}</p>
                  <div className="order-items">
                    <h4>Items</h4>
                    <ul>
                      {order.items && order.items.map((item) => (
                        <li key={`${order.order_id}-${item.food_item_id}`}>
                          {item.quantity} x {getFoodItemDisplayName(item, foodItems)} @ ${formatMoney(item.price_per_item || item.price)}
                        </li>
                      ))}
                    </ul>
                  </div>
                  {/* Add review button and form for completed orders */}
                  {canReviewOrder(order) && (
                    <div className="review-section">
                      {!reviewForms[order.order_id]?.open ? (
                        <button type="button" onClick={() => handleOpenReviewForm(order.order_id)}>
                          Leave a Review
                        </button>
                      ) : (
                        <form className="review-form" onSubmit={(e) => { e.preventDefault(); handleSubmitReview(order); }}>
                          <label>
                            Rating:
                            <select
                              value={reviewForms[order.order_id]?.rating || 5}
                              onChange={(e) => handleReviewInputChange(order.order_id, 'rating', e.target.value)}
                            >
                              {[5, 4, 3, 2, 1].map((val) => (
                                <option key={val} value={val}>{val}</option>
                              ))}
                            </select>
                          </label>
                          <label>
                            Review:
                            <textarea
                              value={reviewForms[order.order_id]?.review || ''}
                              onChange={(e) => handleReviewInputChange(order.order_id, 'review', e.target.value)}
                              required
                            />
                          </label>
                          <button type="submit" disabled={reviewForms[order.order_id]?.submitting}>Submit Review</button>
                          <button type="button" onClick={() => handleCloseReviewForm(order.order_id)}>Cancel</button>
                          {reviewForms[order.order_id]?.error && (
                            <p className="error-text">{reviewForms[order.order_id].error}</p>
                          )}
                        </form>
                      )}
                    </div>
                  )}
                </article>
              ))}
            </div>
          )}
        </section>

        {auth && auth.role === 'STAFF' && staffAccessibleRestaurants.length === 0 && (
          <section className="card">
            <h2>Create Your Restaurant</h2>
            <p>Create a restaurant first to unlock inventory and food item management for your staff account.</p>
            {restaurantCreateError && <p className="error-text">{restaurantCreateError}</p>}
            {restaurantCreateMessage && <p className="success-text">{restaurantCreateMessage}</p>}
            <form className="food-form" onSubmit={handleCreateRestaurant}>
              <div className="form-grid">
                <label>
                  Restaurant name
                  <input
                    type="text"
                    value={newRestaurantName}
                    onChange={(event) => setNewRestaurantName(event.target.value)}
                    required
                  />
                </label>
                <label>
                  Cuisine
                  <input
                    type="text"
                    value={newRestaurantCuisine}
                    onChange={(event) => setNewRestaurantCuisine(event.target.value)}
                    required
                  />
                </label>
                <label>
                  Address
                  <input
                    type="text"
                    value={newRestaurantAddress}
                    onChange={(event) => setNewRestaurantAddress(event.target.value)}
                    required
                  />
                </label>
                <label>
                  Open hour
                  <input
                    type="time"
                    value={newRestaurantOpenHour}
                    onChange={(event) => setNewRestaurantOpenHour(event.target.value)}
                    required
                  />
                </label>
                <label>
                  Closed hour
                  <input
                    type="time"
                    value={newRestaurantClosedHour}
                    onChange={(event) => setNewRestaurantClosedHour(event.target.value)}
                    required
                  />
                </label>
              </div>
              <div className="form-actions">
                <button type="submit">Create Restaurant</button>
              </div>
            </form>
          </section>
        )}

        {auth && auth.role === 'STAFF' && canManageRestaurant && staffAccessibleRestaurants.length > 0 && (
          <section className="card">
            <h2>Inventory Management</h2>
            {inventoryError && <p className="error-text">{inventoryError}</p>}
            <div className="inventory-grid">
              {managedInventoryItems.map((item) => {
                const itemId = item.food_item_id ?? item.id;
                const itemInventory = inventory[itemId];
                const itemDraft = inventoryDrafts[itemId] ?? (itemInventory?.quantity != null ? String(itemInventory.quantity) : '');
                return (
                  <article key={itemId} className="inventory-card">
                    <h3>{item.food_name ?? item.name ?? 'Unnamed item'}</h3>
                    <p><strong>Restaurant:</strong> {item.restaurant_id}</p>
                    <p><strong>Price:</strong> ${formatMoney(item.price)}</p>
                    <p><strong>Saved Stock:</strong> {itemInventory?.quantity ?? 'Not loaded yet'}</p>
                    <div className="inventory-controls">
                      <label>
                        New Stock Value
                        <input
                          type="number"
                          min="0"
                          value={itemDraft}
                          placeholder={itemInventory ? '' : 'Click Load Inventory first'}
                          onChange={(event) => {
                            const rawValue = event.target.value;
                            if (rawValue === '') {
                              setInventoryDrafts((prev) => ({ ...prev, [itemId]: '' }));
                              return;
                            }
                            const newQuantity = Math.max(0, Number(rawValue) || 0);
                            setInventoryDrafts((prev) => ({ ...prev, [itemId]: String(newQuantity) }));
                          }}
                        />
                      </label>
                      <button
                        type="button"
                        onClick={() => {
                          if (itemInventory == null && itemDraft === '') {
                            loadInventoryForFoodItem(itemId);
                            return;
                          }
                          handleUpdateInventory(itemId, Math.max(0, Number(itemDraft) || 0));
                        }}
                      >
                        {itemInventory == null ? 'Load Inventory' : 'Update Inventory'}
                      </button>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        )}

        {auth && auth.role === 'STAFF' && canManageRestaurant && staffAccessibleRestaurants.length > 0 && (
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
                    <input
                      type="text"
                      value={activeStaffRestaurant ? `${activeStaffRestaurant.restaurant_name} (${activeStaffRestaurant.restaurant_id})` : ''}
                      readOnly
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
                <div className="form-header-actions">
                  <h3>Edit Food Item: {editingFoodItem.food_name}</h3>
                  <div className="form-actions">
                    <button type="submit">Update Food Item</button>
                    <button type="button" onClick={handleCancelEdit}>
                      Cancel
                    </button>
                  </div>
                </div>
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
                <label
                  className="inventory-quantity-field"
                  style={{ width: '140px', minWidth: '140px', maxWidth: '140px', overflow: 'hidden' }}
                >
                  Inventory Quantity
                  <input
                    type="text"
                    inputMode="numeric"
                    pattern="[0-9]*"
                    style={{ width: '140px', minWidth: '140px', maxWidth: '140px', boxSizing: 'border-box' }}
                    value={newFoodInventoryQuantity}
                    onChange={(event) => {
                      const sanitizedValue = event.target.value.replace(/\D/g, '');
                      setNewFoodInventoryQuantity(sanitizedValue);
                    }}
                    required
                  />
                </label>
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
              {!loadingFoodManagement && managedFoodItems.length === 0 && (
                <p>No food items found.</p>
              )}
              {!loadingFoodManagement && managedFoodItems.length > 0 && (
                managedFoodItems.map((item) => (
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

        {auth && auth.role === 'STAFF' && canManageRestaurant && ownerRestaurant && (
          <section className="card">
            <h2>Staff Assignment Management</h2>
            {renderStaffAssignmentManager()}
          </section>
        )}

        {auth && auth.role === 'STAFF' && canManageRestaurant && selectedStaffRestaurantId && (
          <section className="card">
            <h2>Restaurant Order Management</h2>
            {renderRestaurantOrderManager()}
          </section>
        )}

        {auth && auth.role === 'STAFF' && isCourierOnly && (
          <section className="card">
            <h2>Courier Delivery Management</h2>
            {renderCourierOrderManager()}
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

            <section className="card">
                <h2>Most Ordered</h2>

            {!auth && <p>Log in to view most ordered restaurants.</p>}
            {auth && loadingMostOrdered && <p>Loading most ordered...</p>}
            {auth && mostOrderedError && (
            <p className="error-text">{mostOrderedError}</p>
            )}
            {auth && !loadingMostOrdered && mostOrdered.length === 0 && (
          <p>No restaurant stats available.</p>
            )}
            {auth && !loadingMostOrdered && mostOrdered.length > 0 && (
          <div className="favorite-orders-list">
          {mostOrdered
          .filter(
          (stat) =>
            typeof stat.restaurant_name === "string" &&
            stat.restaurant_name.trim() !== ""
        )
        .map((stat, index) => (
          <article key={index} className="favorite-order-card">
            <div className="order-header">
              <h3>{stat.restaurant_name}</h3>
            </div>

            <p>
              <strong>Orders:</strong> {stat.order_count}
            </p>
            </article>
            ))}
          </div>
        )}
          </section>

      <section className="card">
  <h2>Most Ordered Food Items</h2>

  {!auth && <p>Log in to view food stats.</p>}

  {auth && loadingFoodStats && <p>Loading food stats...</p>}

  {auth && foodStatsError && (
    <p className="error-text">{foodStatsError}</p>
  )}

  {auth && !loadingFoodStats && foodStats.length === 0 && (
    <p>No food stats available.</p>
  )}

  {auth && !loadingFoodStats && foodStats.length > 0 && (
    <div className="favorite-orders-list">
      {foodStats
        .filter(
          (stat) =>
            typeof stat.food_name === "string" &&
            stat.food_name.trim() !== ""
        )
        .map((stat, index) => (
          <article key={index} className="favorite-order-card">
            <div className="order-header">
              <h3>{stat.food_name}</h3>
            </div>

            <p>
              <strong>Food ID:</strong> {stat.food_item_id}
            </p>

            <p>
              <strong>Orders:</strong> {stat.order_count}
            </p>
          </article>
        ))}
    </div>
  )}
</section>

         
          </>
      
      </main>
    </div>
  );
}

export default App;
