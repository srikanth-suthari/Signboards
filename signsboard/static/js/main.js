// Urban Services JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Back to top button
    const backToTopButton = document.createElement('button');
    backToTopButton.className = 'back-to-top';
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(backToTopButton);

    // Show/hide back to top button
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    // Back to top click handler
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add fade-in animation to cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe all cards and service items
    document.querySelectorAll('.card, .service-card, .feature-item').forEach(el => {
        observer.observe(el);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            }
        });
    });

    // Price calculator for signboards
    const priceCalculator = document.getElementById('price-calculator');
    if (priceCalculator) {
        const typeSelect = document.getElementById('id_signboard_type');
        const sizeSelect = document.getElementById('id_size');
        const finishSelect = document.getElementById('id_finish');
        const urgencySelect = document.getElementById('id_urgency');
        const priceDisplay = document.getElementById('price-display');

        function calculatePrice() {
            const typeId = typeSelect.value;
            const sizeId = sizeSelect.value;
            const finishId = finishSelect.value;
            const urgency = urgencySelect.value;

            if (typeId && sizeId) {
                fetch(`/signboards/calculate-price/?type_id=${typeId}&size_id=${sizeId}&finish_id=${finishId}&urgency=${urgency}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            priceDisplay.innerHTML = `
                                <div class="price-breakdown">
                                    <div class="d-flex justify-content-between">
                                        <span>Base Cost:</span>
                                        <span>₹${data.base_cost.toFixed(2)}</span>
                                    </div>
                                    ${data.urgency_charges > 0 ? `
                                    <div class="d-flex justify-content-between">
                                        <span>Urgency Charges:</span>
                                        <span>₹${data.urgency_charges.toFixed(2)}</span>
                                    </div>
                                    ` : ''}
                                    <hr>
                                    <div class="d-flex justify-content-between fw-bold">
                                        <span>Total:</span>
                                        <span class="text-success">₹${data.total_cost.toFixed(2)}</span>
                                    </div>
                                </div>
                            `;
                        }
                    })
                    .catch(error => {
                        console.error('Error calculating price:', error);
                    });
            }
        }

        [typeSelect, sizeSelect, finishSelect, urgencySelect].forEach(select => {
            if (select) {
                select.addEventListener('change', calculatePrice);
            }
        });
    }

    // Vehicle fare calculator
    const fareCalculator = document.getElementById('fare-calculator');
    if (fareCalculator) {
        const vehicleSelect = document.getElementById('id_vehicle');
        const bookingTypeSelect = document.getElementById('id_booking_type');
        const distanceInput = document.getElementById('id_estimated_distance_km');
        const durationInput = document.getElementById('id_estimated_duration_hours');
        const fareDisplay = document.getElementById('fare-display');

        function calculateFare() {
            const vehicleId = vehicleSelect.value;
            const bookingType = bookingTypeSelect.value;
            const distance = distanceInput.value || 0;
            const duration = durationInput.value || 0;

            if (vehicleId && bookingType) {
                fetch(`/vehicles/calculate-fare/?vehicle_id=${vehicleId}&booking_type=${bookingType}&distance_km=${distance}&duration_hours=${duration}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            fareDisplay.innerHTML = `
                                <div class="fare-breakdown">
                                    <div class="d-flex justify-content-between">
                                        <span>Base Fare:</span>
                                        <span>₹${data.base_fare.toFixed(2)}</span>
                                    </div>
                                    <div class="d-flex justify-content-between">
                                        <span>Distance Charges:</span>
                                        <span>₹${data.distance_fare.toFixed(2)}</span>
                                    </div>
                                    ${data.time_fare > 0 ? `
                                    <div class="d-flex justify-content-between">
                                        <span>Time Charges:</span>
                                        <span>₹${data.time_fare.toFixed(2)}</span>
                                    </div>
                                    ` : ''}
                                    ${data.additional_charges > 0 ? `
                                    <div class="d-flex justify-content-between">
                                        <span>Additional Charges:</span>
                                        <span>₹${data.additional_charges.toFixed(2)}</span>
                                    </div>
                                    ` : ''}
                                    <hr>
                                    <div class="d-flex justify-content-between fw-bold">
                                        <span>Total Fare:</span>
                                        <span class="text-success">₹${data.total_fare.toFixed(2)}</span>
                                    </div>
                                </div>
                            `;
                        }
                    })
                    .catch(error => {
                        console.error('Error calculating fare:', error);
                    });
            }
        }

        [vehicleSelect, bookingTypeSelect, distanceInput, durationInput].forEach(input => {
            if (input) {
                input.addEventListener('change', calculateFare);
                input.addEventListener('input', calculateFare);
            }
        });
    }

    // Cart quantity updater
    const cartItems = document.querySelectorAll('.cart-item');
    cartItems.forEach(item => {
        const quantityInput = item.querySelector('.quantity-input');
        const updateBtn = item.querySelector('.update-quantity');
        
        if (quantityInput && updateBtn) {
            quantityInput.addEventListener('change', function() {
                const form = this.closest('form');
                if (form) {
                    form.submit();
                }
            });
        }
    });

    // Image preview for file uploads
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = input.parentNode.querySelector('.file-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'file-preview mt-2';
                        input.parentNode.appendChild(preview);
                    }
                    
                    if (file.type.startsWith('image/')) {
                        preview.innerHTML = `<img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px;">`;
                    } else {
                        preview.innerHTML = `<p class="text-muted">File selected: ${file.name}</p>`;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Search form enhancement
    const searchForms = document.querySelectorAll('.search-form');
    searchForms.forEach(form => {
        const searchInput = form.querySelector('input[type="search"]');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    // Auto-submit search after 500ms of no typing
                    if (this.value.length >= 3 || this.value.length === 0) {
                        form.submit();
                    }
                }, 500);
            });
        }
    });

    // Rating display enhancement
    const ratingElements = document.querySelectorAll('.rating-display');
    ratingElements.forEach(element => {
        const rating = parseInt(element.dataset.rating);
        const maxRating = parseInt(element.dataset.maxRating) || 5;
        
        let stars = '';
        for (let i = 1; i <= maxRating; i++) {
            if (i <= rating) {
                stars += '<i class="fas fa-star text-warning"></i>';
            } else {
                stars += '<i class="far fa-star text-muted"></i>';
            }
        }
        element.innerHTML = stars;
    });

    // Tooltip initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Modal handling
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            // Focus first input when modal opens
            const firstInput = this.querySelector('input, textarea, select');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        });
    });
});
