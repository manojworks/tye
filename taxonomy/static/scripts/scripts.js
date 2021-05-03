function makeTableOnLoad() {
    $.when(
        getNumberOfPages()
    ).then(function (){
        startRow = 0;
        endRow = document.getElementById("maxRows").value;
        fetchTaxonomy(startRow, endRow);
    })

}

function makeTableNavButtons() {
    // get the total number of rows
    let numRowsReturned = document.getElementById("numRows").value;
    let numRowsPerPage =  document.getElementById("maxRows").value;
    var showFrom = 0
    var showTo = numRowsPerPage

    jQuery(function($) {

        $("#pagination").pagination({

            items: numRowsReturned,
            itemsOnPage: numRowsPerPage,
            cssStyle: "light-theme",

            // This is the actual page changing functionality.
            onPageClick: function(pageNumber) {
                // We need to show and hide `tr`s appropriately.
                showFrom = numRowsPerPage * (pageNumber - 1);
                showTo = showFrom + parseInt(numRowsPerPage);

                fetchTaxonomy(showFrom, showTo)
            }
            });
        })
}

function fetchTaxonomy(startRow, endRow) {
    console.log('start ' + startRow)
    console.log('end ' + endRow)

    $.ajax({
        type: 'GET',
        url: "get/ajax/validate/list",
        data: {"startRow": startRow,
                "endRow": endRow},
        success: function (response) {
            let i;
            var tbdy = document.getElementById('gen_tbl').getElementsByTagName('tbody')[0];
            var tbl = document.getElementById('gen_tbl')

            $(".var-table").find("tr:not(:first)").remove();

            let taxonomy_json = $.parseJSON(response);
            const len = Object.keys(taxonomy_json).length
            const all_ids = Object.keys(taxonomy_json)
            for (i = 0; i < len; i++) {
                var pid = all_ids[i]
                var new_row = tbdy.insertRow(-1)
                new_row.innerHTML = "<td>" + pid + "</td><td>" + taxonomy_json[pid] + "</td>"
                tbl.append(new_row)
            }

        },
        error: function (response) {
            console.log(response)
        }
    }).done(function () {
        makeTableNavButtons()
    })
}

getPagination()


function getNumberOfPages() {
    $.ajax({
        type: 'GET',
        url: "get/ajax/validate/taxonomyListSize"
    }).done(function (data){
        document.getElementById("numRows").value = data
    }).fail(function (errMessage){
        console.log("Error in getting number of pages : " + errMessage)
    });
}

function getPagination() {
    $(document).ready(function (){
        $('#maxRows').change(function (){
            let numRows = parseInt($(this).val());
            if (numRows == 5000) {
                numRows = -1
            }
            fetchTaxonomy(0, numRows);
        })

    })
}