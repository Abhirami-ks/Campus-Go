// notifications.js
const notificationsSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
  );
  
  notificationsSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    // Handle the notification message received from the server
    console.log('New notification:', data.message);
  };
  