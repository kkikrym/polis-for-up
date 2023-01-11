function timelinehistory(mq){
    const articles = document.querySelectorAll("#ArticleBox");
    const dates = document.querySelectorAll("#created_at");
    const timeNow=new Date();
    const yesterday = new Date(timeNow.getFullYear(), timeNow.getMonth(), timeNow.getDate()-1, timeNow.getHours(), timeNow.getMinutes(), timeNow.getSeconds());
    const withinHour = new Date(timeNow.getFullYear(), timeNow.getMonth(), timeNow.getDate(), timeNow.getHours()-1, timeNow.getMinutes(), timeNow.getSeconds());
    for (let i=0; i<dates.length; i++) {
        let ca = dates[i].innerHTML.split(' ');
        let created_at = new Date(ca[0], ca[1]-1, ca[2], ca[3], ca[4], ca[5]);
        let div = '<div class="font-08 color-top my-3">'

        if(created_at.getTime() > withinHour.getTime()){ //投稿が一時間以内であれば
            let diff = timeNow.getMinutes() - created_at.getMinutes();
            if (diff<0){
                diff = timeNow.getMinutes() + (60-created_at.getMinutes());
            }
            let w = document.querySelector("#Wrapper"+i);
            if (mq.matches){
                w.style = "border-left:1px solid rgb(173, 173, 173, 0.4)";
            } else{
                w.style = "display:flex; justify-content:center";
            }
            w.insertAdjacentHTML('beforeBegin',
                div + diff +'分前</span>'
            );
        } else if (created_at.getTime() > yesterday.getTime()){ // 投稿が1日以内であれば
            let diff = timeNow.getHours() - created_at.getHours();
            if (diff<0){
                diff = timeNow.getHours() + (24-created_at.getHours());
            }
            let w = document.querySelector("#Wrapper"+i);
            if (mq.matches){
                w.style = "border-left:1px solid rgb(173, 173, 173, 0.4)";
            } else{
                w.style = "display:flex; justify-content:center";
            }
            w.insertAdjacentHTML('beforeBegin',
                div + diff +'時間前</span>'
            );
        } else {
            let diff = Math.round((timeNow.getTime() - created_at.getTime())/ 1000 / 60 / 60 / 24);
            let w = document.querySelector("#Wrapper"+i);
            if (mq.matches){
                w.style = "border-left:1px solid rgb(173, 173, 173, 0.4)";
            } else{
                w.style = "display:flex; justify-content:center";
            }
            w.insertAdjacentHTML('beforeBegin',
                div + diff +'日前</div>'
            );
        }
    }
}
function ifPC() {
    const mq = window.matchMedia('(min-width: 576px)');
    document.addEventListener('DOMContentLoaded', function(){
        timelinehistory(mq);
    }, false);
    const Wrappers = document.querySelectorAll("[id^=Wrapper]")
    function adjustTL(){
        for (let i=0; i<Wrappers.length; i++){
            if (mq.matches){
                Wrappers[i].style.borderLeft = "1px solid rgb(173, 173, 173, 0.4)";
                Wrappers[i].style.display = "";
                Wrappers[i].style.display.justifyContent = "left";
            } else{
                Wrappers[i].style.borderLeft = "0px solid white";
                Wrappers[i].style.display = "flex";
                Wrappers[i].style.display.justifyContent = "center";
            }
        }
    }
    mq.addEventListener('change', adjustTL, false);
}
ifPC()