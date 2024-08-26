$(document).ready(function() {
    // Initialize DataTable
    $('#events-table').DataTable({
        "order": [[0, "desc"]],
        "paging": true,
        "searching": true,
        "info": true,
        "autoWidth": false,
        "language": {
            "emptyTable": "No data available in table"
        }
    });

    // Select/Deselect all checkboxes
    $('#select-all').on('click', function() {
        $('input[name="selected_events"]').prop('checked', this.checked);
    });
});