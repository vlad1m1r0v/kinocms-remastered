function restructureDatatable() {
    const $dtLength = $('.dt-length');
    const $dtSearch = $('.dt-search');
    $dtLength.wrap('<div class="col-md-auto mr-auto"></div>');
    $dtSearch.wrap('<div class="col-md-auto ml-auto"></div>');

    const $dtInfo = $('.dt-info');
    const $dtPaging = $('.dt-paging');
    $dtInfo.wrap('<div class="col-md-auto mr-auto"></div>');
    $dtPaging.wrap('<div class="col-md-auto ml-auto"></div>');

    const firstRow = $('<div class="row justify-content-between"></div>')
        .append($dtLength.parent())
        .append($dtSearch.parent());

    const secondRow = $('<div class="row justify-content-between mb-2"></div>')
        .append($dtInfo.parent())
        .append($dtPaging.parent());

    const tableId = $('table').prop('id');

    firstRow.insertBefore(`#${tableId}`);
    secondRow.insertAfter(`#${tableId}`);

    const $table = $(`#${tableId}`);
    $table.wrap('<div style="overflow-x: auto"></div>');
}
