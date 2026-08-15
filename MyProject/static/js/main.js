document.addEventListener('DOMContentLoaded', function() {
    // --- Modal Elements ---
    const modal = document.getElementById('redirect-modal');
    // Get URLs from Django context
    const djangoUrlsElement = document.getElementById('django-urls-data');
    const djangoUrls = djangoUrlsElement ? JSON.parse(djangoUrlsElement.textContent) : {};

    const modalTitle = document.getElementById('modal-title');
    const modalMessage = document.getElementById('modal-message');
    const modalCountdown = document.getElementById('modal-countdown');
    const modalIconContainer = document.getElementById('modal-icon-container');
    const toastElement = document.getElementById('cart-toast-link');

    // --- Cart Toast Helper Functions ---
    function displayCartToast(toastData) {
        if (!toastElement) return;

        let imagesHTML = '';
        const imagesToDisplay = toastData.cart_images || [];

        if (imagesToDisplay.length > 0) {
            // Reverse for stacking effect (oldest item at the bottom of the visual stack).
            imagesToDisplay.reverse().slice(0, 5).forEach(imgSrc => {
                imagesHTML += `<img src="${imgSrc}">`; // Use the full URL directly
            });
        } else if (toastData.cart_count > 0) {
            imagesHTML = `<div class="toast-icon-wrap"><i class="fa-solid fa-shopping-cart"></i></div>`;
        } else {
            const iconClass = 'fa-solid fa-trash-can';
            imagesHTML = `<div class="toast-icon-wrap"><i class="${iconClass}"></i></div>`;
        }

        const title = toastData.title || (toastData.type === 'cart_add' ? 'Added to Cart!' : 'Item Removed');
        const itemName = toastData.item_name || (toastData.cart_count > 0 ? 'Click to view your cart' : 'Your cart is now empty.');
        const totalItems = toastData.cart_count;

        let countText = `Your cart has <strong>${totalItems}</strong> items.`;
        if (totalItems === 0) {
            countText = '';
        }

        toastElement.innerHTML = `
            <div class="toast-body">
                <div class="toast-images">
                    ${imagesHTML}
                </div>
                <div class="toast-text">
                    <strong class="me-auto d-block">${title}</strong>
                    <div class="text-muted small">${itemName}</div>
                    <div class="text-muted small mt-1">${countText}</div>
                </div>
            </div>
        `;

        toastElement.style.display = 'block';
        toastElement.className = 'cart-toast text-decoration-none'; // Reset classes
        if (toastData.type) {
            toastElement.classList.add(toastData.type);
        }

        setTimeout(() => toastElement.classList.add('show'), 50);
    }

    function hideCartToast() {
        if (!toastElement) return;
        toastElement.classList.remove('show');
        toastElement.addEventListener('transitionend', () => {
            if (!toastElement.classList.contains('show')) {
                toastElement.style.display = 'none';
            }
        }, { once: true });
    }

    // --- Banner Elements ---
    const bannerContainer = document.getElementById('notification-banner-container');

    if (bannerContainer) {
        const banners = bannerContainer.querySelectorAll('.notification-banner');
        let modalTriggered = false;

        banners.forEach((banner, index) => {
            if (modalTriggered) { // If modal is already set to show, remove other messages
                banner.remove();
                return;
            }

            const messageText = banner.textContent.trim();
            let toastData;
            try {
                toastData = JSON.parse(messageText);
            } catch (e) {
                toastData = null;
            }

            // --- Handle Cart Toast Messages ---
            if (toastData && (toastData.type === 'cart_add' || toastData.type === 'cart_remove')) {
                modalTriggered = true; // Prevent other modals/banners
                banner.remove(); // Don't show the raw JSON banner

                if (toastData.cart_count > 0) {
                    displayCartToast(toastData);
                } else {
                    hideCartToast();
                }
                return; // Message handled
            }


            let modalConfig = null;

            // --- Check for Order Success Modal ---
            if (messageText === 'Order placed successfully.') {
                modalTriggered = true;
                banner.remove(); // Don't show this message as a banner

                const orderModal = document.getElementById('order-success-modal');
                const orderSound = document.getElementById('order-success-sound');

                if (orderModal) {
                    orderModal.style.display = 'flex';
                    setTimeout(() => orderModal.classList.add('show'), 10);
                }

                if (orderSound) {
                    orderSound.play().catch(e => console.warn("Audio play failed. User interaction might be required."));
                }

                // Redirect after 2 seconds
                setTimeout(() => {
                    window.location.href = djangoUrls.userProductsUrl || '/user/products/'; // Use dynamic URL
                }, 2000);
                return; // Message handled, skip to next
            }

            // --- Check for Redirect Modal Messages ---
            if (messageText === 'Logged in successfully.') {
                modalConfig = {
                    type: 'success',
                    title: 'Login Successful!',
                    message: 'Welcome back. You are now logged in.',
                    redirect: djangoUrls.customerIndexUrl || '/customer/index/'
                };
            } else if (messageText === 'You have been logged out successfully.') {
                modalConfig = {
                    type: 'success',
                    title: 'Logout Successful!',
                    message: 'You have been securely signed out.',
                    redirect: djangoUrls.userIndexUrl || '/user/index/'
                };
            } else if (messageText.startsWith('Please login')) {
                modalConfig = {
                    type: 'warning',
                    title: 'Authentication Required',
                    message: messageText,
                    redirect: djangoUrls.userLoginUrl || '/user/login/'
                };
            }

            // --- Process Modal or Banner ---
            if (modal && modalConfig) {
                modalTriggered = true;
                banner.remove(); // Don't show this message as a banner

                // Configure and show the modal
                modalTitle.textContent = modalConfig.title;
                modalMessage.textContent = modalConfig.message;
                if (modalConfig.type === 'success') {
                    modalIconContainer.innerHTML = '<i class="fa-solid fa-check-circle icon-success"></i>';
                } else if (modalConfig.type === 'warning') {
                    modalIconContainer.innerHTML = '<i class="fa-solid fa-exclamation-circle icon-warning"></i>';
                }

                modal.style.display = 'flex';
                setTimeout(() => modal.classList.add('show'), 10);

                let countdown = 3;
                modalCountdown.textContent = `Redirecting in ${countdown} seconds...`;

                const interval = setInterval(() => {
                    countdown--;
                    modalCountdown.textContent = `Redirecting in ${countdown} seconds...`;
                    if (countdown <= 0) {
                        clearInterval(interval);
                        window.location.href = modalConfig.redirect;
                    }
                }, 1000);
                setTimeout(() => { window.location.href = modalConfig.redirect; }, 3100); // Fallback redirect

            } else {
                // --- Process as a Banner ---
                setTimeout(() => {
                    banner.classList.add('show');
                }, 100 * (index + 1));

                setTimeout(() => {
                    banner.classList.remove('show');
                    banner.addEventListener('transitionend', () => banner.remove(), { once: true });
                }, 3000 + (100 * (index + 1)));
            }
        });
    }

    // --- New Add to Cart & Quantity Control Logic ---

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
    const csrftoken = getCookie('csrftoken');

    // Core AJAX function to update cart
    async function updateCartItem(productId, quantity) {
        try {
            const response = await fetch(djangoUrls.updateCartItemUrl || '/user/update_cart_item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    'product_id': productId,
                    'quantity': quantity
                })
            });

            const data = await response.json();

            if (!response.ok) {
                if (response.status === 401 && modal) { // Handle not logged in
                    modalTitle.textContent = 'Authentication Required';
                    modalMessage.textContent = data.message || 'Please login to manage your cart.';
                    modalIconContainer.innerHTML = '<i class="fa-solid fa-exclamation-circle icon-warning"></i>';
                    modal.style.display = 'flex';
                    setTimeout(() => modal.classList.add('show'), 10);
                    setTimeout(() => { window.location.href = djangoUrls.userLoginUrl || '/user/login/'; }, 3000);
                    return null; // Gracefully exit after handling 401
                }
                // For other errors, throw to be caught and logged
                throw new Error(data.message || 'An error occurred on the server.');
            }
            
            // Update UI based on successful response
            const cartBadge = document.getElementById('cart-count-badge');
            if (cartBadge) {
                cartBadge.textContent = data.cart_count;
            }

            if (data.cart_count > 0) {
                displayCartToast(data);
            } else {
                hideCartToast();
            }
            
            return data;

        } catch (error) {
            console.error('Failed to update cart:', error);
            return null;
        }
    }

    // UI update functions
    function showQuantityControls(productControlsEl, quantity) {
        productControlsEl.querySelector('.add-to-cart-container').style.display = 'none';
        const qtyContainer = productControlsEl.querySelector('.quantity-control-container');
        qtyContainer.style.display = 'block';
        qtyContainer.querySelector('.quantity-input').value = quantity;
    }

    function showAddToCartButton(productControlsEl) {
        productControlsEl.querySelector('.add-to-cart-container').style.display = 'block';
        productControlsEl.querySelector('.quantity-control-container').style.display = 'none';
    }

    // Initialization on page load
    function initializeProductControls() {
        const cartQuantitiesData = document.getElementById('cart-quantities-data');
        if (!cartQuantitiesData) return;

        const cartQuantities = JSON.parse(cartQuantitiesData.textContent);
        document.querySelectorAll('.product-controls').forEach(control => {
            const productId = control.dataset.pid;
            if (cartQuantities[productId] && cartQuantities[productId] > 0) {
                showQuantityControls(control, cartQuantities[productId]);
            } else {
                showAddToCartButton(control);
            }
        });
    }

    // Event Delegation for all product controls
    document.body.addEventListener('click', function(event) {
        const addToCartBtn = event.target.closest('.add-to-cart-btn');
        const quantityBtn = event.target.closest('.quantity-btn');

        if (addToCartBtn) {
            const productControls = addToCartBtn.closest('.product-controls');
            if (productControls) {
                const productId = productControls.dataset.pid;
                updateCartItem(productId, 1).then(data => {
                    if (data && data.status === 'success') {
                        showQuantityControls(productControls, 1);
                    }
                });
            }
        } else if (quantityBtn) {
            const productControls = quantityBtn.closest('.product-controls');
            if (productControls) {
                const productId = productControls.dataset.pid;
                const quantityInput = productControls.querySelector('.quantity-input');
                let currentQuantity = parseInt(quantityInput.value, 10);
                let newQuantity = (quantityBtn.dataset.action === 'increment') ? currentQuantity + 1 : currentQuantity - 1;

                if (newQuantity < 0) newQuantity = 0;

                updateCartItem(productId, newQuantity).then(data => {
                    if (data && data.status === 'success') {
                        if (newQuantity > 0) {
                            quantityInput.value = newQuantity;
                        } else {
                            showAddToCartButton(productControls);
                        }
                    }
                });
            }
        }
    });

    // --- Initial Page Load Logic for Sticky Toast ---
    function initializeStickyToast() {
        const cartBadge = document.getElementById('cart-count-badge');
        if (!cartBadge) return;

        const cartCount = parseInt(cartBadge.textContent.trim(), 10) || 0;
        
        if (cartCount > 0) {
            const cartImagesData = document.getElementById('cart-images-data');
            if (!cartImagesData) return;

            const cartImages = JSON.parse(cartImagesData.textContent);
            const toastData = {
                cart_count: cartCount,
                cart_images: cartImages,
                title: "You have items in your cart",
            };
            displayCartToast(toastData);
        }
    }
    initializeStickyToast();
    initializeProductControls();
});