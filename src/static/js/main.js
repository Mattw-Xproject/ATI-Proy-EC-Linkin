// Toggle notifications dropdown
        function toggleNotifications() {
            const dropdown = document.getElementById('notificationsDropdown');
            dropdown.classList.toggle('active');
            
            // Cerrar si se hace click fuera
            if (dropdown.classList.contains('active')) {
                document.addEventListener('click', closeNotificationsOutside);
            } else {
                document.removeEventListener('click', closeNotificationsOutside);
            }
        }
        
        function closeNotificationsOutside(event) {
            const dropdown = document.getElementById('notificationsDropdown');
            const notificationItem = event.target.closest('.navbar-item');
            
            if (!dropdown.contains(event.target) && !notificationItem) {
                dropdown.classList.remove('active');
                document.removeEventListener('click', closeNotificationsOutside);
            }
        }
        
        // Marcar todas como leídas
        function markAllAsRead(event) {
            event.preventDefault();
            event.stopPropagation();
            
            fetch('{% url "mark_all_notifications_read" %}', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar badge
                    const badge = document.getElementById('notificationsBadge');
                    if (badge) {
                        badge.remove();
                    }
                    
                    // Recargar dropdown
                    window.location.reload();
                }
            })
            .catch(error => console.error('Error:', error));
        }
        
        // Actualizar contador de notificaciones cada 30 segundos
        
        function updateNotificationsCount() {
            fetch('{% url "notifications_count" %}')
                .then(response => response.json())
                .then(data => {
                    const badge = document.getElementById('notificationsBadge');
                    
                    if (data.count > 0) {
                        if (badge) {
                            badge.textContent = data.count;
                        } else {
                            // Crear badge si no existe
                            const notifItem = document.querySelector('.navbar-item:has(i.bi-bell-fill)');
                            if (notifItem) {
                                const newBadge = document.createElement('span');
                                newBadge.className = 'notification-badge';
                                newBadge.id = 'notificationsBadge';
                                newBadge.textContent = data.count;
                                notifItem.appendChild(newBadge);
                            }
                        }
                    } else {
                        if (badge) {
                            badge.remove();
                        }
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        
        // Actualizar cada 30 segundos
        setInterval(updateNotificationsCount, 30000);
        