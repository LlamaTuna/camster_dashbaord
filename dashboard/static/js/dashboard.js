$(document).ready(function() {
    console.log("DataTables initialization script running");  // Add this line to debug
    $('#events-table').DataTable({
        "order": [[ 0, "desc" ]],  // By default, order by the first column (Timestamp) in descending order
        "paging": true,             // Enable pagination
        "searching": true,          // Enable search/filtering
        "info": true,               // Show table information
        "autoWidth": false          // Disable auto width to ensure proper alignment
    });
});
