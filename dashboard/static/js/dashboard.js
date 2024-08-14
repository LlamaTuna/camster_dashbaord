$(document).ready(function() {
    $('#events-table').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        autoWidth: false,
        pageLength: 10,
        lengthChange: false,
        language: {
            emptyTable: "No events found"
        }
    });
});
