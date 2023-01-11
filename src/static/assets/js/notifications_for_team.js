function notificationsForTeam(){
    document.addEventListener("DOMContentLoaded", function(){
        const n_threads = JSON.parse(document.getElementById('n_threads').textContent);
        const ts = Object.keys(n_threads);
        let num = 0;
        for (item in n_threads) {
            if (n_threads[item]){
                if (n_threads[item] != '0'){
                        const name = '#n_' + ts[num];
                        const n = document.querySelector(name);
                        n.innerHTML = '<span class="notification-team d-block">' + '<span class="intbox">' + n_threads[item] + '</span>' + '</span>';
                    }
                }
            num += 1;
        }
    }
    );
};
notificationsForTeam();