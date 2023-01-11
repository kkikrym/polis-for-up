function pl() {
    let target = document.querySelectorAll("#plus-minus");
    for ( i in target) {
        item = target[i];
        inner = parseFloat(item.innerHTML);
        if (inner< 0) {
            item.style.color = "red";
        } else if (inner>=0) {
            item.style.color = "blue";
            item.insertAdjacentHTML('afterbegin', '+ ');
        }
    }
}

pl()