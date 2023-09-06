function sortTable(table, columnIndex, ascending = true) {
    const direction = ascending ? 1 : -1;                 // if its ascending, direction is 1, else is -1
    const header = $('th:nth-child('+columnIndex+')');    // gets the header with index columnIndex
    const body = table.children[1]                        // gets the body (second children of table)
    const rows = Array.from(body.querySelectorAll("tr")); // creates an array for the rows in the body 

    // removes previous order from every header
    table.querySelectorAll("th").forEach(th => th.classList.remove("ascending", "descending"));

    // adds the order to the clicked header
    header[0].classList.toggle("ascending", ascending);
    header[0].classList.toggle("descending", !ascending);

    // algorithm for sorting the rows
    const sorted = rows.sort((a, b) => {
        const aColumn = a.querySelector('td:nth-child('+columnIndex+')').textContent;
        const bColumn = b.querySelector('td:nth-child('+columnIndex+')').textContent;

        return aColumn > bColumn ? (1*direction) : (-1*direction);
    });

    // removes the rows from the body and add the sorted rows
	while (body.firstChild) {
		body.removeChild(body.firstChild);
	}
	body.append(...sorted);
    
}
        
console.log('hello world');

document.querySelectorAll("table th").forEach(header => {
    header.addEventListener("click", () => {
        const table = header.parentElement.parentElement.parentElement;
        const columnIndex = Array.prototype.indexOf.call(header.parentElement.children, header);
        const isAscending = header.classList.contains("ascending");
        sortTable(table, columnIndex+1 , !isAscending);
    });
});
