function vwchange(){
    document.addEventListener('DOMContentLoaded', function(){
    const PhoneTab = document.querySelectorAll("#PhoneTab");
    const PcTab = document.querySelectorAll("#PcTab");
    const mq = window.matchMedia('(min-width: 576px)');
    // article tree-history for pc and smartphone
    if (document.querySelector('#ArticleRow')){
        function TreeHistory(mq){
            const articles = document.querySelectorAll("#ArticleRow");
            const dates = document.querySelectorAll("#ArticleDate");
            let m = parseInt(dates[0].innerHTML.split('/')[1]) + 1;
            let c = 0;
            for (let i=0; i<dates.length; i++) {
                let ca = parseInt(dates[i].innerHTML.split('/')[1]);
                let Y = dates[i].innerHTML.split('/')[0];
                if ( ca != m){
                    m -= 1;
                    if (mq.matches){
                        articles[i].insertAdjacentHTML('beforeBegin',
                            '<p class="color-top my-2">' +
                                dates[i].innerHTML.split('/')[0] + '年' + dates[i].innerHTML.split('/')[1] + '月' +
                            '</p>' +
                            '<div class="row mx-2" style="border-left: 1px solid grey" id="wrapper' + Y + '/' + m  + '"></div>'
                        );
                    } else{
                        articles[i].insertAdjacentHTML('beforeBegin',
                            '<p class="color-top my-2">' +
                                dates[i].innerHTML.split('/')[0] + '年' + dates[i].innerHTML.split('/')[1] + '月' +
                            '</p>' +
                            '<div class="row justify-content-center mx-2" style="border-left: 1px solid grey" id="wrapper' + Y + '/' + m  + '"></div>'
                        );
                    }
                }
                let h = articles[i].style.height;
                let s = 'wrapper'+Y+'/'+m;
                let r = document.getElementById(s);
                r.appendChild(articles[i])
            }
        }
        TreeHistory(mq);
    }
    const wrappers = document.querySelectorAll("[id^='wrapper']");
    function PcPhone(mq){
        if (mq.matches) {
            //PC
            for (let p=0;p<PcTab.length;p++) { PcTab[p].style.display = 'unset'; };
            for (let p=0;p<PhoneTab.length;p++) { PhoneTab[p].style.display = 'none'; };
            for (let p=0;p<wrappers.length;p++) { console.log('aaa'); wrappers[p].classList.remove('justify-content-center'); };
        } else {
            //SmartPhone
            for (let p=0;p<PcTab.length;p++) { PcTab[p].style.display = 'none'; };
            for (let p=0;p<PhoneTab.length;p++) { PhoneTab[p].style.display = 'unset'; };
            for (let p=0;p<wrappers.length;p++) { console.log('bbb'); wrappers[p].classList.add('justify-content-center');};
        }
    }
    PcPhone(mq);
    mq.addEventListener('change', PcPhone, false);
}, false);

}

vwchange();