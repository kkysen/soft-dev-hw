import * as $ from "jquery";
function identity(t) {
    return t;
}
class TableSorter {
    constructor(selector, startRow, endRow) {
        this.table = $(selector).find("tbody");
        this.rows = this.table.find("tr");
        this.startRow = startRow;
        if (endRow < 0) {
            endRow = this.rows.length - endRow;
        }
        this.endRow = endRow;
    }
    bindColumn(selector, key) {
        TableSorter.sortColumn(this.table, this.rows, selector, key, this.startRow, this.endRow);
    }
    static sortColumn(_table, _rows, _selector, _key, _startRow, _endRow) {
        const table = _table;
        const rows = _rows;
        const selector = _selector;
        const key = _key;
        const startRow = _startRow;
        const endRow = _endRow;
        const parse = function (value) {
            return key($(value).children("td").eq(column).text());
        };
        let order = 1;
        const sort = function () {
            rows.slice(startRow, endRow).sort(function (e1, e2) {
                const t1 = parse(e1);
                const t2 = parse(e2);
                return t1 === t2 ? 0 : t1 < t2 ? -order : order;
            }).appendTo(table);
        };
        const columnHeader = $(selector);
        const column = $(columnHeader).prevAll().length;
        columnHeader.click(function () {
            sort();
            order *= -1;
        });
    }
}
const occupationsTable = new TableSorter("#occupations-table", 1, -1);
occupationsTable.bindColumn("#occupation-column", identity);
occupationsTable.bindColumn("#percent-column", i => parseFloat(i.slice(0, i.length - 1)));
