// NutriFlow AI Frontend Controller - Full Map, Live GPS Geocoding & Calorie-Targeted Delivery
const API_BASE = '/api/v1';

let currentHealthProfile = {
  age: 25,
  gender: 'male',
  height_cm: 174,
  weight_kg: 80,
  activity_level: 'moderate',
  goal: 'weight_loss',
  diet_preference: 'vegetarian'
};

let currentDayPlan = null;
let cart = [];
let activeOrderId = 101;
const orderStages = ['step-placed', 'step-preparing', 'step-out', 'step-delivered'];

// Map & GPS Tracking variables
let map = null;
let bigModalMap = null;
let kitchenMarker = null;
let destinationMarker = null;
let riderMarker = null;
let routePolyline = null;

let modalKitchenMarker = null;
let modalDestMarker = null;
let modalRiderMarker = null;
let modalRoutePolyline = null;

let currentRouteIndex = 1;
let currentDeliveryStatus = 'OUT_FOR_DELIVERY';

// Default coordinates: Sector 14 Kitchen to Sector 16C Dwarka
let kitchenCoords = [28.5921, 77.0460];
let customerCoords = [28.5995, 77.0180];
let currentGPSRoute = [];

const AUTO_RESTAURANTS = {
  'vegetarian': { 
    name: 'NutriFlow Pure Green Kitchen', 
    location: 'Sector 14, Dwarka', 
    coords: [28.5921, 77.0460],
    rating: '4.9 ★', 
    prepTime: 10,
    specialty: '100% Vegetarian & Clean Macros'
  },
  'vegan': { 
    name: 'GreenFuel Organic Plant Kitchen', 
    location: 'Sector 12, Dwarka', 
    coords: [28.5910, 77.0390],
    rating: '4.8 ★', 
    prepTime: 12,
    specialty: '100% Plant-Based & Organic'
  },
  'keto': { 
    name: 'KetoCrafters Gourmet Cloud Kitchen', 
    location: 'Sector 10, Dwarka', 
    coords: [28.5830, 77.0540],
    rating: '4.9 ★', 
    prepTime: 15,
    specialty: 'Ultra-Low Carb & Healthy Fats'
  },
  'non_vegetarian': { 
    name: 'FitGrill High-Protein Kitchen', 
    location: 'Sector 14 North, Dwarka', 
    coords: [28.5980, 77.0420],
    rating: '4.9 ★', 
    prepTime: 12,
    specialty: 'Lean Meats & High Bioavailable Protein'
  },
  'any': { 
    name: 'NutriFlow Master Cloud Kitchen', 
    location: 'Sector 14, Dwarka', 
    coords: [28.5921, 77.0460],
    rating: '4.9 ★', 
    prepTime: 10,
    specialty: 'Precision Calorie-Targeted Nutrition'
  }
};

document.addEventListener('DOMContentLoaded', async () => {
  lucide.createIcons();
  generateCurrentRoute();
  initDeliveryMap();
  await loadDayPlan();
});

// Haversine distance calculation in KM
function calculateDistanceKm(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return Math.max(0.5, +(R * c).toFixed(1));
}

// Generate interpolated realistic waypoints between kitchen and customer
function generateCurrentRoute() {
  const start = kitchenCoords;
  const end = customerCoords;
  const steps = 6;
  const route = [];
  
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const curveOffset = Math.sin(t * Math.PI) * 0.002;
    const lat = start[0] + (end[0] - start[0]) * t + curveOffset;
    const lon = start[1] + (end[1] - start[1]) * t - (curveOffset * 0.5);
    route.push([lat, lon]);
  }
  currentGPSRoute = route;
  return route;
}

// Initialize Home Small Map
function initDeliveryMap() {
  const mapElement = document.getElementById('delivery-map');
  if (!mapElement) return;

  map = L.map('delivery-map').setView([28.5960, 77.0320], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map);

  const createIcon = (emoji, bgClass) => L.divIcon({
    className: 'custom-div-icon',
    html: `<div class="w-10 h-10 rounded-full ${bgClass} text-white flex items-center justify-center text-lg shadow-lg border-2 border-white">${emoji}</div>`,
    iconSize: [40, 40],
    iconAnchor: [20, 20]
  });

  kitchenMarker = L.marker(kitchenCoords, { icon: createIcon('🍳', 'bg-emerald-600') }).addTo(map)
    .bindPopup('<b>NutriFlow Cloud Kitchen</b><br>Sector 14 Dwarka');

  destinationMarker = L.marker(customerCoords, { icon: createIcon('🏠', 'bg-rose-600') }).addTo(map)
    .bindPopup('<b>Your Delivery Address</b><br>Sector 16C Dwarka');

  routePolyline = L.polyline(currentGPSRoute, {
    color: '#059669',
    weight: 5,
    opacity: 0.8,
    dashArray: '8, 8'
  }).addTo(map);

  riderMarker = L.marker(currentGPSRoute[currentRouteIndex], {
    icon: L.divIcon({
      className: 'custom-rider-icon',
      html: `<div class="w-11 h-11 rounded-full bg-slate-900 text-white flex items-center justify-center text-xl shadow-2xl border-2 border-amber-400 pulse-rider">🛵</div>`,
      iconSize: [44, 44],
      iconAnchor: [22, 22]
    })
  }).addTo(map).bindPopup('<b>Rahul Sharma (Delivery Partner)</b><br>En route on TVS Raider');

  map.fitBounds(L.latLngBounds([kitchenCoords, customerCoords]), { padding: [30, 30] });
}

// Initialize and Open Big Modal Map Window
function openBigMapModal() {
  const modal = document.getElementById('big-map-modal');
  if (!modal) return;
  modal.classList.remove('hidden');
  updateBigModalSummary();

  // Force multiple size recalculations for Leaflet to render tiles inside modal
  initBigModalMap();
}

function initBigModalMap() {
  const container = document.getElementById('big-modal-map');
  if (!container) return;

  if (!bigModalMap) {
    bigModalMap = L.map('big-modal-map', {
      zoomControl: true,
      attributionControl: true
    }).setView(kitchenCoords, 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19
    }).addTo(bigModalMap);

    const createIcon = (emoji, bgClass) => L.divIcon({
      className: 'custom-div-icon',
      html: `<div class="w-10 h-10 rounded-full ${bgClass} text-white flex items-center justify-center text-lg shadow-lg border-2 border-white">${emoji}</div>`,
      iconSize: [40, 40],
      iconAnchor: [20, 20]
    });

    modalKitchenMarker = L.marker(kitchenCoords, { icon: createIcon('🍳', 'bg-emerald-600') }).addTo(bigModalMap)
      .bindPopup('<b>NutriFlow Cloud Kitchen</b><br>Sector 14 Dwarka');

    modalDestMarker = L.marker(customerCoords, { 
      icon: createIcon('🏠', 'bg-rose-600'),
      draggable: true 
    }).addTo(bigModalMap).bindPopup('<b>Your Delivery Destination</b><br><span class="text-xs text-slate-500">Drag pin to set location!</span>');

    modalDestMarker.on('dragend', async (e) => {
      const { lat, lng } = e.target.getLatLng();
      await onLocationChanged(lat, lng, true);
    });

    modalRoutePolyline = L.polyline(currentGPSRoute, {
      color: '#059669',
      weight: 6,
      opacity: 0.85,
      dashArray: '6, 6'
    }).addTo(bigModalMap);

    modalRiderMarker = L.marker(currentGPSRoute[currentRouteIndex], {
      icon: L.divIcon({
        className: 'custom-rider-icon',
        html: `<div class="w-12 h-12 rounded-full bg-slate-900 text-white flex items-center justify-center text-2xl shadow-2xl border-2 border-amber-400 pulse-rider">🛵</div>`,
        iconSize: [48, 48],
        iconAnchor: [24, 24]
      })
    }).addTo(bigModalMap).bindPopup('<b>Rahul Sharma (Rider)</b><br>En Route');

    bigModalMap.on('click', async (e) => {
      const { lat, lng } = e.latlng;
      await onLocationChanged(lat, lng, true);
    });
  }

  // Force Leaflet tile engine to resize and render
  const refreshMap = () => {
    if (bigModalMap) {
      bigModalMap.invalidateSize(true);
      if (kitchenCoords && customerCoords) {
        bigModalMap.fitBounds(L.latLngBounds([kitchenCoords, customerCoords]), { padding: [40, 40] });
      }
    }
  };

  refreshMap();
  setTimeout(refreshMap, 100);
  setTimeout(refreshMap, 300);
  setTimeout(refreshMap, 600);
  lucide.createIcons();
}

function closeBigMapModal() {
  const modal = document.getElementById('big-map-modal');
  if (modal) modal.classList.add('hidden');
}

// Show feedback message banner
function showGpsStatus(message, isSuccess = true) {
  const banner = document.getElementById('gps-status-banner');
  const msgEl = document.getElementById('gps-status-msg');
  const iconEl = document.getElementById('gps-status-icon');
  if (!banner || !msgEl) return;

  banner.classList.remove('hidden', 'bg-emerald-50', 'border-emerald-200', 'text-emerald-800', 'bg-amber-50', 'border-amber-200', 'text-amber-800');
  if (isSuccess) {
    banner.classList.add('bg-emerald-50', 'border-emerald-200', 'text-emerald-800');
    if (iconEl) iconEl.innerText = '✅';
  } else {
    banner.classList.add('bg-amber-50', 'border-amber-200', 'text-amber-800');
    if (iconEl) iconEl.innerText = '⚠️';
  }
  msgEl.innerText = message;
}

// Quick Preset Location Selection
async function setPresetLocation(addressName, lat, lon) {
  const input = document.getElementById('modal-address-input');
  if (input) input.value = addressName;
  document.getElementById('delivery-address-text').innerText = addressName;
  await onLocationChanged(lat, lon, false);
  showGpsStatus(`Delivery location set to: ${addressName}`, true);
}

// Central handler when location coords change (via GPS, Drag, Click or Preset)
async function onLocationChanged(lat, lon, reverseGeocodeAddress = true) {
  customerCoords = [lat, lon];

  // Move destination markers
  if (modalDestMarker) modalDestMarker.setLatLng([lat, lon]);
  if (destinationMarker) destinationMarker.setLatLng([lat, lon]);

  // Regenerate route
  generateCurrentRoute();
  
  if (routePolyline) routePolyline.setLatLngs(currentGPSRoute);
  if (modalRoutePolyline) modalRoutePolyline.setLatLngs(currentGPSRoute);

  // Pan / Fit
  if (bigModalMap) {
    bigModalMap.invalidateSize(true);
    bigModalMap.fitBounds(L.latLngBounds([kitchenCoords, customerCoords]), { padding: [40, 40] });
  }
  if (map) {
    map.invalidateSize(true);
    map.fitBounds(L.latLngBounds([kitchenCoords, customerCoords]), { padding: [30, 30] });
  }

  // Update summary & ETA
  updateBigModalSummary();

  // Reverse geocode street address using OpenStreetMap Nominatim
  if (reverseGeocodeAddress) {
    await fetchReverseGeocode(lat, lon);
  }
}

// Free OpenStreetMap Nominatim Reverse Geocoding
async function fetchReverseGeocode(lat, lon) {
  try {
    const inputEl = document.getElementById('modal-address-input');
    if (inputEl) inputEl.placeholder = 'Fetching street address...';

    const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&addressdetails=1`;
    const res = await fetch(url, { headers: { 'Accept-Language': 'en' } });
    if (!res.ok) throw new Error('Geocoding service unavailable');
    
    const data = await res.json();
    const addr = data.address || {};
    
    // Construct readable Indian street address
    const parts = [
      addr.road || addr.pedestrian || addr.suburb || addr.neighbourhood,
      addr.residential || addr.commercial || addr.subdistrict,
      addr.city || addr.town || addr.district || 'New Delhi',
      addr.postcode
    ].filter(Boolean);

    const formattedAddress = parts.length > 0 ? parts.join(', ') : (data.display_name || '').split(',').slice(0, 4).join(',');
    
    if (formattedAddress) {
      if (inputEl) inputEl.value = formattedAddress;
      document.getElementById('delivery-address-text').innerText = formattedAddress;
      showGpsStatus(`Resolved Address: ${formattedAddress}`, true);
    }
    
    if (modalDestMarker) {
      modalDestMarker.bindPopup(`<b>Your Delivery Destination</b><br><span class="text-xs text-slate-700">${formattedAddress || 'Selected Pin'}</span>`).openPopup();
    }
  } catch (err) {
    console.warn('Reverse geocode fallback:', err);
    const fallback = `Pin Location (${lat.toFixed(4)}, ${lon.toFixed(4)})`;
    const inputEl = document.getElementById('modal-address-input');
    if (inputEl) inputEl.value = fallback;
    document.getElementById('delivery-address-text').innerText = fallback;
    showGpsStatus(`Pin Location set to (${lat.toFixed(4)}, ${lon.toFixed(4)})`, true);
  }
}

// Live GPS Location Detection (Using navigator.geolocation with fallback)
async function detectLiveGPSLocation() {
  const btn = document.getElementById('gps-detect-btn');
  const btnText = document.getElementById('gps-btn-text');

  if (btn) btn.disabled = true;
  if (btnText) btnText.innerHTML = `<span class="animate-spin mr-1">⏳</span> Locating...`;
  showGpsStatus('📡 Contacting device GPS sensor...', true);

  if (!navigator.geolocation) {
    if (btn) btn.disabled = false;
    if (btnText) btnText.innerText = 'Use Current GPS';
    showGpsStatus('⚠️ Geolocation not supported by this browser. Use presets or type address.', false);
    return;
  }

  // Fast Geolocation attempt
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      try {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        await onLocationChanged(lat, lon, true);
        showGpsStatus(`📍 Live GPS Detected: (${lat.toFixed(4)}, ${lon.toFixed(4)})`, true);
      } catch (e) {
        console.warn('GPS handling error:', e);
      } finally {
        if (btn) btn.disabled = false;
        if (btnText) btnText.innerText = 'Use Current GPS';
        lucide.createIcons();
      }
    },
    async (error) => {
      console.warn('GPS Error/Timeout:', error);
      let errorMsg = 'GPS signal unavailable on this device/network.';
      if (error.code === error.PERMISSION_DENIED) {
        errorMsg = 'Location permission was denied in browser settings.';
      } else if (error.code === error.TIMEOUT) {
        errorMsg = 'GPS request timed out. Using high-precision New Delhi NCR preset.';
      }

      // Smooth fallback to Delhi NCR preset without hanging
      await onLocationChanged(28.5995, 77.0180, true);
      showGpsStatus(`⚠️ ${errorMsg} Auto-centered map to Sector 16C Dwarka.`, false);

      if (btn) btn.disabled = false;
      if (btnText) btnText.innerText = 'Use Current GPS';
      lucide.createIcons();
    },
    { enableHighAccuracy: false, timeout: 5000, maximumAge: 300000 }
  );
}

// User Address Update Handler (Manual text entry)
async function handleAddressUpdate() {
  const baseAddress = document.getElementById('modal-address-input').value.trim();
  const houseNo = document.getElementById('modal-house-no').value.trim();
  const landmark = document.getElementById('modal-landmark').value.trim();

  if (!baseAddress) {
    alert('Please enter a valid street address.');
    return;
  }

  const fullDisplay = [houseNo, landmark, baseAddress].filter(Boolean).join(', ');
  document.getElementById('delivery-address-text').innerText = fullDisplay;

  // Try forward geocoding the address using OpenStreetMap Nominatim
  try {
    const searchUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(baseAddress)}&limit=1`;
    const res = await fetch(searchUrl, { headers: { 'Accept-Language': 'en' } });
    const data = await res.json();
    
    if (data && data.length > 0) {
      const lat = parseFloat(data[0].lat);
      const lon = parseFloat(data[0].lon);
      await onLocationChanged(lat, lon, false);
      showGpsStatus(`Route updated for "${fullDisplay}"`, true);
    }
  } catch (err) {
    console.warn('Forward geocoding fallback:', err);
  }

  showGpsStatus(`Delivery address updated to "${fullDisplay}"`, true);
}

let currentMealVariation = 0;

// Fetch complete day plan and health metrics from FastAPI backend
async function loadDayPlan(variation = 0) {
  try {
    const payload = {
      ...currentHealthProfile,
      variation: variation
    };
    const res = await fetch(`${API_BASE}/recommendations/day-plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to fetch day plan');
    currentDayPlan = await res.json();
    renderDashboard();
    renderMeals();
    renderWorkout();
    updateBigModalSummary();
    lucide.createIcons();
  } catch (err) {
    console.error(err);
  }
}

// Render Dashboard Metrics
function renderDashboard() {
  if (!currentDayPlan) return;
  const h = currentDayPlan.health_summary;

  document.getElementById('profile-summary-text').innerText = 
    `Age ${currentHealthProfile.age} • ${currentHealthProfile.gender.toUpperCase()} • ${currentHealthProfile.weight_kg}kg • ${currentHealthProfile.height_cm}cm • Goal: ${formatGoal(currentHealthProfile.goal)}`;

  document.getElementById('bmi-value').innerText = h.bmi;
  document.getElementById('bmi-category').innerText = h.bmi_category;
  document.getElementById('bmi-card').style.borderLeftColor = h.bmi_status_color;

  document.getElementById('bmr-value').innerText = Math.round(h.bmr).toLocaleString();
  document.getElementById('tdee-value').innerText = Math.round(h.tdee).toLocaleString();
  document.getElementById('target-cal-value').innerText = Math.round(h.target_daily_calories).toLocaleString();
  
  if (h.calorie_adjustment < 0) {
    document.getElementById('calorie-goal-subtext').innerText = `${h.calorie_adjustment} kcal deficit (Fat Loss)`;
    document.getElementById('calorie-goal-subtext').className = 'text-xs font-medium text-amber-600';
  } else if (h.calorie_adjustment > 0) {
    document.getElementById('calorie-goal-subtext').innerText = `+${h.calorie_adjustment} kcal surplus (Muscle Hypertrophy)`;
    document.getElementById('calorie-goal-subtext').className = 'text-xs font-medium text-emerald-600';
  } else {
    document.getElementById('calorie-goal-subtext').innerText = `Maintenance Energy Equilibrium`;
    document.getElementById('calorie-goal-subtext').className = 'text-xs font-medium text-blue-600';
  }

  document.getElementById('health-advice-banner').innerText = h.health_advice;

  // Render Macros
  document.getElementById('macro-protein').innerHTML = `${currentDayPlan.total_plan_protein}g <span class="text-xs font-normal text-slate-500">(${Math.round(currentDayPlan.total_plan_protein * 4)} kcal)</span>`;
  document.getElementById('macro-carbs').innerHTML = `${currentDayPlan.total_plan_carbs}g <span class="text-xs font-normal text-slate-500">(${Math.round(currentDayPlan.total_plan_carbs * 4)} kcal)</span>`;
  document.getElementById('macro-fat').innerHTML = `${currentDayPlan.total_plan_fat}g <span class="text-xs font-normal text-slate-500">(${Math.round(currentDayPlan.total_plan_fat * 9)} kcal)</span>`;
}

// Render Meal Cards (With Indian Rupee ₹ Prices)
function renderMeals() {
  const container = document.getElementById('meal-cards-container');
  if (!currentDayPlan || !currentDayPlan.meals) return;

  container.innerHTML = currentDayPlan.meals.map(m => {
    const food = m.recommended_food;
    const dietBadgeColor = food.diet_type === 'vegan' ? 'bg-green-100 text-green-800' :
                           food.diet_type === 'vegetarian' ? 'bg-emerald-100 text-emerald-800' :
                           food.diet_type === 'keto' ? 'bg-purple-100 text-purple-800' : 'bg-amber-100 text-amber-800';

    return `
      <div class="glass-card rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition flex flex-col border border-slate-200">
        <div class="relative h-44 overflow-hidden bg-slate-100">
          <img src="${food.image_url}" alt="${food.name}" class="w-full h-full object-cover hover:scale-105 transition duration-500">
          <span class="absolute top-3 left-3 px-2.5 py-1 rounded-full bg-slate-900/80 backdrop-blur text-white text-xs font-bold uppercase tracking-wider">
            ${m.category}
          </span>
          <span class="absolute top-3 right-3 px-2.5 py-1 rounded-full ${dietBadgeColor} text-xs font-bold uppercase">
            ${food.diet_type.replace('_', ' ')}
          </span>
        </div>

        <div class="p-5 flex-grow flex flex-col justify-between space-y-4">
          <div class="space-y-1.5">
            <h4 class="font-bold text-slate-900 text-base leading-snug">${food.name}</h4>
            <p class="text-xs text-slate-500 line-clamp-2">${food.description}</p>
          </div>

          <!-- MACRO BADGES -->
          <div class="grid grid-cols-4 gap-1.5 text-center bg-slate-50 p-2.5 rounded-xl border border-slate-100 text-[11px]">
            <div>
              <p class="text-slate-400 font-semibold text-[10px]">CALS</p>
              <p class="font-bold text-slate-800">${food.calories}</p>
            </div>
            <div>
              <p class="text-blue-500 font-semibold text-[10px]">PROT</p>
              <p class="font-bold text-blue-900">${food.protein_g}g</p>
            </div>
            <div>
              <p class="text-amber-500 font-semibold text-[10px]">CARB</p>
              <p class="font-bold text-amber-900">${food.carbs_g}g</p>
            </div>
            <div>
              <p class="text-rose-500 font-semibold text-[10px]">FAT</p>
              <p class="font-bold text-rose-900">${food.fat_g}g</p>
            </div>
          </div>

          <div class="flex items-center justify-between pt-2 border-t border-slate-100">
            <div>
              <span class="text-xs text-slate-400">Price</span>
              <p class="text-base font-extrabold text-emerald-700">₹${Math.round(food.price)}</p>
            </div>
            <button onclick="addToCart(${food.id}, '${escapeQuotes(food.name)}', ${food.price}, ${food.calories}, '${food.image_url}', '${m.category}')" 
              class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md shadow-emerald-600/20 transition flex items-center space-x-1">
              <i data-lucide="plus" class="w-3.5 h-3.5"></i>
              <span>Add Meal</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// Render Workout Routine
function renderWorkout() {
  if (!currentDayPlan || !currentDayPlan.workout) return;
  const w = currentDayPlan.workout;
  document.getElementById('workout-title').innerText = w.title;
  document.getElementById('workout-duration').innerText = `${w.duration_mins} mins`;
  document.getElementById('workout-intensity').innerText = w.intensity;
  document.getElementById('workout-description').innerText = w.description;

  const exContainer = document.getElementById('workout-exercises-list');
  exContainer.innerHTML = w.exercises.map(ex => `
    <div class="flex items-center space-x-3 p-3 rounded-xl bg-slate-50 border border-slate-200/70 text-xs font-semibold text-slate-800">
      <div class="w-6 h-6 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center flex-shrink-0">
        <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
      </div>
      <span>${ex}</span>
    </div>
  `).join('');
}

// Floating Toast Notification System
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  const bgClass = type === 'success' ? 'bg-slate-900/95 text-white border-emerald-500/40' :
                  type === 'warning' ? 'bg-amber-950/95 text-amber-100 border-amber-500/40' :
                  'bg-rose-950/95 text-rose-100 border-rose-500/40';
  const icon = type === 'success' ? '🥗' : type === 'warning' ? '⚠️' : '❌';

  toast.className = `pointer-events-auto transform translate-y-2 opacity-0 transition-all duration-300 flex items-center justify-between p-3.5 rounded-2xl ${bgClass} border backdrop-blur-md shadow-2xl space-x-3 text-xs font-semibold`;
  toast.innerHTML = `
    <div class="flex items-center space-x-2.5">
      <span class="text-base">${icon}</span>
      <span>${message}</span>
    </div>
    <button onclick="this.parentElement.remove()" class="text-slate-400 hover:text-white p-1 ml-2">✕</button>
  `;

  container.appendChild(toast);
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');
  });

  setTimeout(() => {
    toast.classList.add('opacity-0', '-translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Clear Entire Cart
function clearCart() {
  cart = [];
  updateCartUI();
  updateBigModalSummary();
  showToast('Cart cleared', 'warning');
}

// Cart System (In Indian Rupees ₹)
function addToCart(id, name, price, calories, image, category = '', suppressDrawer = false) {
  const existing = cart.find(item => item.id === id);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ id, name, price, calories, image, category, quantity: 1 });
  }
  updateCartUI();
  updateBigModalSummary();
  if (!suppressDrawer) {
    toggleCart(true);
    showToast(`Added "${name}" (₹${Math.round(price)}) to cart!`, 'success');
  }
}

function addAllMealsToCart() {
  if (!currentDayPlan || !currentDayPlan.meals || currentDayPlan.meals.length === 0) {
    showToast('Please wait for meal plan to finish loading!', 'warning');
    return;
  }

  // Add all 4 prescribed meals (Breakfast, Lunch, Dinner, Snack)
  currentDayPlan.meals.forEach(m => {
    const f = m.recommended_food;
    const existing = cart.find(item => item.id === f.id);
    if (existing) {
      existing.quantity += 1;
    } else {
      cart.push({
        id: f.id,
        name: f.name,
        price: f.price,
        calories: f.calories,
        image: f.image_url,
        category: m.category,
        quantity: 1
      });
    }
  });

  updateCartUI();
  updateBigModalSummary();
  toggleCart(true); // Smoothly slide open cart drawer

  const totalCals = Math.round(currentDayPlan.total_plan_calories);
  const totalPrice = Math.round(currentDayPlan.meals.reduce((sum, m) => sum + m.recommended_food.price, 0));
  showToast(`🛒 Full Day Plan (All 4 Meals • ${totalCals} kcal • ₹${totalPrice}) added to your cart!`, 'success');
}

function updateCartUI() {
  const count = cart.reduce((acc, item) => acc + item.quantity, 0);
  const totalCals = cart.reduce((acc, item) => acc + (item.calories * item.quantity), 0);
  const totalPrice = cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);

  const badge = document.getElementById('cart-badge');
  if (count > 0) {
    badge.innerText = count;
    badge.classList.remove('hidden');
  } else {
    badge.classList.add('hidden');
  }

  document.getElementById('cart-total-calories').innerText = `${Math.round(totalCals)} kcal`;
  document.getElementById('cart-total-price').innerText = `₹${Math.round(totalPrice)}`;

  const container = document.getElementById('cart-items-container');
  if (cart.length === 0) {
    container.innerHTML = `
      <div class="text-center py-12 text-slate-400 space-y-3">
        <i data-lucide="utensils" class="w-12 h-12 mx-auto text-slate-300"></i>
        <p class="text-sm">Your delivery cart is empty.</p>
        <button onclick="addAllMealsToCart()" class="text-xs font-bold text-emerald-600 hover:underline">Add recommended day plan</button>
      </div>
    `;
  } else {
    container.innerHTML = cart.map(item => `
      <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200 shadow-sm">
        <div class="flex items-center space-x-3">
          <img src="${item.image}" alt="${item.name}" class="w-12 h-12 rounded-xl object-cover shadow-sm">
          <div>
            <div class="flex items-center space-x-1.5">
              <p class="font-bold text-xs text-slate-900 leading-tight">${item.name}</p>
              ${item.category ? `<span class="text-[9px] px-1.5 py-0.5 rounded bg-slate-200 text-slate-700 font-bold uppercase">${item.category}</span>` : ''}
            </div>
            <p class="text-[11px] text-slate-500 mt-0.5">${item.calories} kcal • <strong class="text-emerald-700">₹${Math.round(item.price)}</strong></p>
          </div>
        </div>
        <div class="flex items-center space-x-1.5 bg-white border border-slate-200 rounded-lg p-1">
          <button onclick="changeQty(${item.id}, -1)" class="w-6 h-6 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center font-bold text-xs transition">-</button>
          <span class="text-xs font-bold px-1.5 text-slate-800">${item.quantity}</span>
          <button onclick="changeQty(${item.id}, 1)" class="w-6 h-6 rounded bg-emerald-100 hover:bg-emerald-200 text-emerald-800 flex items-center justify-center font-bold text-xs transition">+</button>
        </div>
      </div>
    `).join('');
  }
  lucide.createIcons();
}

function changeQty(id, delta) {
  const item = cart.find(i => i.id === id);
  if (!item) return;
  item.quantity += delta;
  if (item.quantity <= 0) {
    cart = cart.filter(i => i.id !== id);
  }
  updateCartUI();
  updateBigModalSummary();
}

function toggleCart(forceOpen = null) {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-overlay');
  const isOpen = !drawer.classList.contains('translate-x-full');
  const shouldOpen = forceOpen !== null ? forceOpen : !isOpen;

  if (shouldOpen) {
    drawer.classList.remove('translate-x-full');
    overlay.classList.remove('hidden');
  } else {
    drawer.classList.add('translate-x-full');
    overlay.classList.add('hidden');
  }
}

// Checkout & Order Placement
async function handleCheckout() {
  if (cart.length === 0) return alert('Your cart is empty!');

  const address = document.getElementById('modal-address-input').value || "Sector 16C, Dwarka, Delhi";
  const orderPayload = {
    customer_name: "Ansh Mishra",
    delivery_address: address,
    phone_number: "+91-9876543210",
    items: cart.map(item => ({ food_item_id: item.id, quantity: item.quantity }))
  };

  try {
    const res = await fetch(`${API_BASE}/orders/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderPayload)
    });
    if (!res.ok) throw new Error('Order creation failed');
    const order = await res.json();
    activeOrderId = order.id;
    document.getElementById('active-order-id-badge').innerText = `Order #${order.id}`;
    cart = [];
    updateCartUI();
    toggleCart(false);
    updateDeliveryUI('PLACED');
    updateBigModalSummary();
    alert(`🎉 Order #${order.id} Placed Successfully!\nTotal: ₹${Math.round(order.total_amount)} (${order.total_calories} kcal)\nTracking live on map!`);
    openBigMapModal();
  } catch (err) {
    alert('Error placing order: ' + err.message);
  }
}

// Live Delivery Progression Simulation on Map
async function advanceActiveOrder() {
  try {
    const res = await fetch(`${API_BASE}/orders/${activeOrderId}/advance-status`, {
      method: 'POST'
    });
    if (!res.ok) {
      cycleLocalDeliveryStatus();
      return;
    }
    const order = await res.json();
    updateDeliveryUI(order.status);
  } catch (err) {
    cycleLocalDeliveryStatus();
  }
}

let currentLocalStatusIdx = 1;
function cycleLocalDeliveryStatus() {
  const statuses = ['PLACED', 'PREPARING', 'OUT_FOR_DELIVERY', 'DELIVERED'];
  currentLocalStatusIdx = (currentLocalStatusIdx + 1) % statuses.length;
  updateDeliveryUI(statuses[currentLocalStatusIdx]);
}

function updateDeliveryUI(status) {
  const mapBadge = document.getElementById('map-status-badge');
  const etaBadge = document.getElementById('map-eta-badge');
  const modalMapStatus = document.getElementById('modal-map-status');

  const statusMap = {
    'PLACED': { step: 0, label: '📋 Order Confirmed & Queued', eta: '30 mins', waypoint: 0 },
    'PREPARING': { step: 1, label: '🍳 Kitchen Cooking Fresh Macros', eta: '20 mins', waypoint: 1 },
    'OUT_FOR_DELIVERY': { step: 2, label: '🛵 Rider On The Way', eta: '10 mins', waypoint: 3 },
    'DELIVERED': { step: 3, label: '🎉 Delivered at Doorstep', eta: '0 mins', waypoint: currentGPSRoute.length - 1 }
  };

  const info = statusMap[status] || statusMap['PREPARING'];
  if (mapBadge) mapBadge.innerText = info.label;
  if (etaBadge) etaBadge.innerText = info.eta;
  if (modalMapStatus) modalMapStatus.innerText = `${info.label} (${info.eta})`;

  const targetCoord = currentGPSRoute[Math.min(info.waypoint, currentGPSRoute.length - 1)];

  // Move Rider on Home Map
  if (riderMarker && map) {
    riderMarker.setLatLng(targetCoord);
    map.panTo(targetCoord, { animate: true, duration: 1.2 });
  }

  // Move Rider on Big Modal Map
  if (modalRiderMarker && bigModalMap) {
    modalRiderMarker.setLatLng(targetCoord);
    bigModalMap.panTo(targetCoord, { animate: true, duration: 1.2 });
    if (status === 'DELIVERED') {
      modalRiderMarker.bindPopup('<b>Delivered!</b><br>Enjoy your nutritious meal!').openPopup();
    } else {
      modalRiderMarker.bindPopup(`<b>Rahul Sharma</b><br>${info.label} (ETA: ${info.eta})`).openPopup();
    }
  }

  // Update 4-step indicator
  orderStages.forEach((stepId, idx) => {
    const el = document.getElementById(stepId);
    if (el) {
      if (idx <= info.step) {
        el.classList.remove('opacity-40');
        const circle = el.querySelector('div');
        circle.className = 'w-9 h-9 mx-auto rounded-full bg-emerald-600 text-white flex items-center justify-center shadow';
      } else {
        el.classList.add('opacity-40');
        const circle = el.querySelector('div');
        circle.className = 'w-9 h-9 mx-auto rounded-full bg-slate-300 text-slate-700 flex items-center justify-center';
      }
    }
  });
  lucide.createIcons();
}

// AI Nutritionist Chat Handler
async function handleAICoachSubmit(e) {
  e.preventDefault();
  const input = document.getElementById('ai-prompt-input');
  const query = input.value.trim();
  if (!query) return;

  const chatContainer = document.getElementById('ai-chat-history');
  
  // Add user bubble
  chatContainer.innerHTML += `
    <div class="flex items-start space-x-2.5 justify-end">
      <div class="bg-slate-900 text-white p-3 rounded-2xl rounded-tr-none text-xs sm:text-sm max-w-xl">
        ${escapeHTML(query)}
      </div>
      <div class="w-7 h-7 rounded-full bg-slate-800 text-white flex items-center justify-center text-xs flex-shrink-0">You</div>
    </div>
  `;
  input.value = '';
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const res = await fetch(`${API_BASE}/ai-coach/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_goal: currentHealthProfile.goal,
        daily_calories: currentDayPlan ? currentDayPlan.health_summary.target_daily_calories : 2240,
        question: query,
        diet_preference: currentHealthProfile.diet_preference
      })
    });
    const data = await res.json();

    chatContainer.innerHTML += `
      <div class="flex items-start space-x-2.5">
        <div class="w-7 h-7 rounded-full bg-emerald-600 text-white flex items-center justify-center text-xs flex-shrink-0">AI</div>
        <div class="bg-emerald-50 text-emerald-950 p-3 rounded-2xl rounded-tl-none text-xs sm:text-sm max-w-xl">
          ${data.answer.replace(/\n/g, '<br>')}
          <div class="text-[10px] text-emerald-700 font-semibold mt-1">Source: ${data.ai_provider}</div>
        </div>
      </div>
    `;
    chatContainer.scrollTop = chatContainer.scrollHeight;
  } catch (err) {
    console.error(err);
  }
}

// Modal Handlers
function openHealthModal() {
  document.getElementById('health-modal').classList.remove('hidden');
}
function closeHealthModal() {
  document.getElementById('health-modal').classList.add('hidden');
}

async function handleHealthFormSubmit(e) {
  e.preventDefault();
  currentHealthProfile = {
    age: parseInt(document.getElementById('inp-age').value),
    gender: document.getElementById('inp-gender').value,
    height_cm: parseFloat(document.getElementById('inp-height').value),
    weight_kg: parseFloat(document.getElementById('inp-weight').value),
    activity_level: document.getElementById('inp-activity').value,
    goal: document.getElementById('inp-goal').value,
    diet_preference: document.getElementById('inp-diet').value
  };
  closeHealthModal();
  await loadDayPlan();
}

async function refreshMealPlan() {
  const btn = document.getElementById('btn-regenerate-meals');
  const icon = document.getElementById('icon-regenerate-meals');
  const text = document.getElementById('text-regenerate-meals');

  if (icon) icon.classList.add('animate-spin');
  if (text) text.innerText = 'Regenerating...';
  if (btn) btn.disabled = true;

  currentMealVariation += 1;
  await loadDayPlan(currentMealVariation);

  if (icon) icon.classList.remove('animate-spin');
  if (text) text.innerText = 'Regenerate Meals';
  if (btn) btn.disabled = false;

  showToast('✨ Fresh chef meal recommendations generated!', 'success');
  lucide.createIcons();
}

// Helpers
function formatGoal(goal) {
  if (goal === 'weight_loss') return 'Weight Loss (-500 kcal)';
  if (goal === 'muscle_gain') return 'Muscle Hypertrophy (+350 kcal)';
  return 'Maintenance';
}
function escapeQuotes(str) {
  return str.replace(/'/g, "\\'");
}
function escapeHTML(str) {
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag));
}
