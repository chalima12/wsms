function sendAssignmentNotification(assignmentId) {
    // Create an Ajax request.
    var request = new XMLHttpRequest();

    // Set the request method and URL.
    request.open('POST', '/workshop/send_assignment_notification/');

    // Set the request headers.
    request.setRequestHeader('Content-Type', 'application/json');

    // Set the request body.
    request.send(JSON.stringify({
        assignment_id: assignmentId
    }));

    // Handle the response.
    request.onload = function() {
        if (request.status === 200) {
            // The notification was sent successfully.
            alert('Notification sent successfully.');
        } else {
            // There was an error sending the notification.
            alert('An error occurred while sending the notification.');
        }
    };
}
