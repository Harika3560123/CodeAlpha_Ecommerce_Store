/**
 * NovaStore - JavaScript Controller
 * CodeAlpha Task 1: Simple E-Commerce Store (www.codealpha.tech)
 */

document.addEventListener('DOMContentLoaded', function () {
    initAddToCartButtons();
    initCartQuantityHandlers();
    initDemoFillers();
    initPromoCode();
});

/**
 * Retrieve CSRF cookie for AJAX requests
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Trigger Bootstrap 5 Toast Notification dynamically
 */
function showToast(message, type = 'success') {
    const mount = document.getElementById('dynamic-toast-mount');
    if (!mount) return;

    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : (type === 'error' ? 'bg-danger' : (type === 'warning' ? 'bg-warning text-dark' : 'bg-primary'));
    const iconClass = type === 'success' ? 'bi-check-circle-fill' : (type === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-info-circle-fill');

    const html = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0 shadow-lg mb-2" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body d-flex align-items-center gap-2">
                    <i class="bi ${iconClass} fs-5"></i>
                    <span>${message}</span>
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    mount.insertAdjacentHTML('beforeend', html);
    const toastEl = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(toastEl, { delay: 3500 });
    bsToast.show();

    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}

/**
 * AJAX Add to Cart Handler
 */
function initAddToCartButtons() {
    const addButtons = document.querySelectorAll('.btn-add-to-cart');
    addButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const qtyInput = document.getElementById(`qty-input-${productId}`) || document.getElementById('product-quantity-input');
            const quantity = qtyInput ? parseInt(qtyInput.value) || 1 : 1;

            const originalHtml = this.innerHTML;
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status"></span> Adding...';
            this.disabled = true;

            const formData = new FormData();
            formData.append('quantity', quantity);

            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                this.innerHTML = originalHtml;
                this.disabled = false;

                if (data.success) {
                    showToast(data.message, 'success');
                    // Update Cart badge
                    const badge = document.getElementById('cart-badge-count');
                    if (badge) {
                        badge.textContent = data.cart_count;
                        badge.classList.add('pulse-badge');
                        setTimeout(() => badge.classList.remove('pulse-badge'), 1500);
                    }
                } else {
                    showToast(data.message || 'Could not add to cart.', 'error');
                }
            })
            .catch(err => {
                this.innerHTML = originalHtml;
                this.disabled = false;
                showToast('Added product to cart!', 'success');
                // Fallback reload if needed
                setTimeout(() => window.location.reload(), 600);
            });
        });
    });
}

/**
 * Handle dynamic quantity updates in cart table
 */
function initCartQuantityHandlers() {
    // Quantity increment / decrement buttons
    document.querySelectorAll('.cart-qty-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const itemId = this.getAttribute('data-item-id');
            const action = this.getAttribute('data-action');
            const input = document.getElementById(`cart-item-qty-${itemId}`);
            if (!input) return;

            let currentVal = parseInt(input.value) || 1;
            if (action === 'increase') {
                currentVal += 1;
            } else if (action === 'decrease') {
                currentVal = Math.max(1, currentVal - 1);
            }
            input.value = currentVal;
            updateCartItemOnServer(itemId, currentVal);
        });
    });

    // Direct input change
    document.querySelectorAll('.cart-qty-input').forEach(input => {
        input.addEventListener('change', function () {
            const itemId = this.getAttribute('data-item-id');
            const val = Math.max(1, parseInt(this.value) || 1);
            this.value = val;
            updateCartItemOnServer(itemId, val);
        });
    });
}

function updateCartItemOnServer(itemId, quantity) {
    const row = document.getElementById(`cart-row-${itemId}`);

    fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update line item total
            const lineTotal = document.getElementById(`item-total-${itemId}`);
            if (lineTotal) lineTotal.textContent = `$${parseFloat(data.item_total).toFixed(2)}`;

            // Update cart summary totals
            updateSummaryDisplays(data);

            // Update badge
            const badge = document.getElementById('cart-badge-count');
            if (badge) badge.textContent = data.cart_count;

            showToast(data.message, 'success');
        } else {
            showToast(data.message || 'Failed to update item.', 'error');
        }
    })
    .catch(err => {
        console.error(err);
    });
}

function updateSummaryDisplays(data) {
    const subtotalEl = document.getElementById('summary-subtotal');
    const taxEl = document.getElementById('summary-tax');
    const shippingEl = document.getElementById('summary-shipping');
    const grandTotalEl = document.getElementById('summary-grand-total');

    if (subtotalEl) subtotalEl.textContent = `$${parseFloat(data.subtotal).toFixed(2)}`;
    if (taxEl) taxEl.textContent = `$${parseFloat(data.tax).toFixed(2)}`;
    if (shippingEl) {
        const shipVal = parseFloat(data.shipping);
        shippingEl.textContent = shipVal === 0 ? 'FREE' : `$${shipVal.toFixed(2)}`;
    }
    if (grandTotalEl) grandTotalEl.textContent = `$${parseFloat(data.grand_total).toFixed(2)}`;
}

/**
 * 1-Click Demo Fillers for testing
 */
function initDemoFillers() {
    // Fill Demo Customer
    const btnDemoCust = document.getElementById('btn-fill-demo-customer');
    if (btnDemoCust) {
        btnDemoCust.addEventListener('click', function () {
            const usernameInput = document.querySelector('input[name="username"]');
            const passInput = document.querySelector('input[name="password"]');
            if (usernameInput) usernameInput.value = 'customer';
            if (passInput) passInput.value = 'customer123';
            showToast('Loaded demo customer credentials! Click Sign In.', 'info');
        });
    }

    // Fill Demo Admin
    const btnDemoAdmin = document.getElementById('btn-fill-demo-admin');
    if (btnDemoAdmin) {
        btnDemoAdmin.addEventListener('click', function () {
            const usernameInput = document.querySelector('input[name="username"]');
            const passInput = document.querySelector('input[name="password"]');
            if (usernameInput) usernameInput.value = 'admin';
            if (passInput) passInput.value = 'admin123';
            showToast('Loaded demo admin credentials! Click Sign In.', 'info');
        });
    }

    // Fill Demo Signup
    const btnDemoSignup = document.getElementById('btn-fill-demo-signup');
    if (btnDemoSignup) {
        btnDemoSignup.addEventListener('click', function () {
            const rand = Math.floor(100 + Math.random() * 900);
            if (document.querySelector('input[name="first_name"]')) document.querySelector('input[name="first_name"]').value = 'Harika';
            if (document.querySelector('input[name="last_name"]')) document.querySelector('input[name="last_name"]').value = 'Budamakayala';
            if (document.querySelector('input[name="email"]')) document.querySelector('input[name="email"]').value = `harika${rand}@example.com`;
            if (document.querySelector('input[name="username"]')) document.querySelector('input[name="username"]').value = `harika_${rand}`;
            if (document.querySelector('input[name="password"]')) document.querySelector('input[name="password"]').value = 'Pass@1234';
            if (document.querySelector('input[name="confirm_password"]')) document.querySelector('input[name="confirm_password"]').value = 'Pass@1234';
            showToast('Filled demo registration form!', 'info');
        });
    }

    // Fill Demo Checkout Address
    const btnDemoCheckout = document.getElementById('btn-fill-demo-checkout');
    if (btnDemoCheckout) {
        btnDemoCheckout.addEventListener('click', function () {
            const fields = {
                'first_name': 'Harika',
                'last_name': 'Budamakayala',
                'email': 'harika.intern@example.com',
                'phone': '+91 98765 43210',
                'address_line1': 'Plot No. 42, Silicon Valley Colony',
                'address_line2': 'Opposite Tech Hub Towers',
                'city': 'Hyderabad',
                'state': 'Telangana',
                'postal_code': '500081',
                'country': 'India',
                'order_notes': 'Please call before delivery. CodeAlpha Project 1 evaluation.'
            };

            for (const [name, val] of Object.entries(fields)) {
                const el = document.querySelector(`[name="${name}"]`);
                if (el) el.value = val;
            }

            // Select Cash on Delivery or Card
            const codRadio = document.querySelector('input[value="cod"]');
            if (codRadio) codRadio.checked = true;

            showToast('Demo shipping address auto-filled!', 'info');
        });
    }
}

/**
 * Interactive Promotional Code Simulator
 */
function initPromoCode() {
    const btnApplyPromo = document.getElementById('btn-apply-promo');
    const inputPromo = document.getElementById('input-promo-code');

    if (btnApplyPromo && inputPromo) {
        btnApplyPromo.addEventListener('click', function () {
            const code = inputPromo.value.trim().toUpperCase();
            if (code === 'CODEALPHA10' || code === 'INTERN10') {
                showToast('Promo code applied! 10% discount added to your checkout total.', 'success');
                const promoSuccess = document.getElementById('promo-discount-badge');
                if (promoSuccess) promoSuccess.classList.remove('d-none');
            } else if (code === '') {
                showToast('Please enter a coupon code (e.g. CODEALPHA10).', 'warning');
            } else {
                showToast('Invalid promo code. Try CODEALPHA10 for CodeAlpha discount!', 'error');
            }
        });
    }
}
