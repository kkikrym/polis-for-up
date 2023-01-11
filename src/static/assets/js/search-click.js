function SearchClick(){
    if (document.querySelector("#select-query")){
        document.querySelector("#select-query").onchange = function(e){
            document.querySelector("#btn-submit").click();
        }
    }
    document.querySelector("#select-order").onchange = function(e){
        document.querySelector("#btn-submit").click();
    }
};
SearchClick();