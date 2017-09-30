import * as $ from "jquery";

interface Sortable<T> {

    sort(comparator: (t1: T, t2: T) => number): this;

}

interface JQueryCollection extends JQuery<HTMLElement>, Sortable<HTMLElement> {
}

type StringKey<T> = (s: string) => T;

function identity<T>(t: T): T {
    return t;
}

class TableSorter {

    private readonly table: JQueryCollection;
    private readonly rows: JQueryCollection;
    private readonly startRow: number;
    private readonly endRow: number;

    public constructor(selector: string, startRow: number, endRow: number) {
        this.table = $(selector).find("tbody") as JQueryCollection;
        this.rows = this.table.find("tr");
        this.startRow = startRow;

        if (endRow < 0) {
            endRow = this.rows.length - endRow;
        }
        this.endRow = endRow;
    }

    public bindColumn<T>(selector: string, key: StringKey<T>) {
        TableSorter.sortColumn(this.table, this.rows, selector, key, this.startRow, this.endRow);
    }

    private static sortColumn<T>(_table: JQueryCollection, _rows: JQueryCollection, _selector: string, _key: StringKey<T>,
                                 _startRow: number, _endRow: number) {
        const table: JQueryCollection = _table;
        const rows: JQueryCollection = _rows;
        const selector: string = _selector;
        const key: StringKey<T> = _key;
        const startRow: number = _startRow;
        const endRow: number = _endRow;

        type Row = HTMLTableRowElement;

        const parse = function (value: Row): T {
            return key($(value).children("td").eq(column).text());
        };

        let order = 1;
        const sort = function (): void {
            rows.slice(startRow, endRow).sort(
                function (e1: Row, e2: Row): number {
                    const t1: T = parse(e1);
                    const t2: T = parse(e2);
                    return t1 === t2 ? 0 : t1 < t2 ? -order : order;
                }).appendTo(table);
        };

        const columnHeader: JQueryCollection = $(selector) as JQueryCollection;
        const column: number = $(columnHeader).prevAll().length;
        columnHeader.click(function () {
            sort();
            order *= -1;
        });

    }

}

const occupationsTable = new TableSorter("#occupations-table", 1, -1);
occupationsTable.bindColumn("#occupation-column", identity);
occupationsTable.bindColumn("#percent-column", i => parseFloat(i.slice(0, i.length - 1)));