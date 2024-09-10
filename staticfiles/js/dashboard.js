$(document).ready(function() {
    // Initialize DataTable on the element with id 'events-table'
    $('#events-table').DataTable({
        "order": [[0, "desc"]],  // Set default sorting to the first column in descending order
        "paging": true,          // Enable pagination
        "searching": true,       // Enable search functionality
        "info": true,            // Display table information (e.g., showing X of Y entries)
        "autoWidth": false,      // Disable automatic column width adjustment
        "language": {
            "emptyTable": "No data available in table"  // Message displayed when table is empty
        }
    });

    // Select/Deselect all checkboxes when the "Select All" checkbox is clicked
    $('#select-all').on('click', function() {
        // Set the checked property of all checkboxes with name 'selected_events' 
        // to match the state of the "Select All" checkbox
        $('input[name="selected_events"]').prop('checked', this.checked);
    });
});
