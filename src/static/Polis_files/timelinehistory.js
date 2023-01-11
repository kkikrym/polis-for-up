function timelinehistory(){
    const articles = document.querySelectorAll("#ArticleBox");
    const dates = document.querySelectorAll("#created_at");
    const timeNow=new Date();
    const yesterday = new Date(timeNow.getFullYear, timeNow.getMonth+1, timeNow.getDate, timeNow.getHours, timeNow.getMinutes, timeNow.getSeconds);
    for (let i=0; i<dates.length; i++) {
        let ca = dates[i].innerHTML.split(' ');
        let created_at = new Date(ca[0], ca[1]-1, ca[2], ca[3], ca[4], ca[5]);
        // 投稿が1日以内であれば
        if (created_at.getTime() > yesterday.getTime()){
            let diff = timeNow.getHours() - created_at.getHours();
            let w = document.querySelector("#Wrapper"+i);
            w.style = "border-left:1px solid grey";
            w.insertAdjacentHTML('beforeBegin',
                '<span class="color-top my-4">'+ diff +'時間前</span>'
            );
        } else {
            let diff = Math.round((timeNow.getTime() - created_at.getTime())/ 1000 / 60 / 60 / 24)-1;
            let w = document.querySelector("#Wrapper"+i);
            w.style = "border-left:1px solid rgb(173, 173, 173, 0.4)";
            w.insertAdjacentHTML('beforeBegin',
                '<div class="font-08 color-top ms-3 my-3">'+ diff +'日前</div>'
            );
        }
    }
}
timelinehistory()