var stocks_mapping = {};
var stock_names = []
var userAge = -1;
var userWatchist = [];
//localStorage.setItem('age', '22');

$('document').ready(function(){
    if(window.location.href == 'http://127.0.0.1:5500/CS7IS5_adaptive_application_group_project/basicUI/index.html'){
        userAge = parseInt(localStorage.getItem('age'));
        
        adjustColor();
        adjustFontSize();

        $.getJSON('stocks_mapping.json', function(data){
            stocks_mapping = data;
            stock_names = Object.values(stocks_mapping);
            console.log(stock_names);
        });

        // autocomplete for searchbar
        $('#stock-searchbar').autocomplete({
            source: stock_names
        });

        // submit event for searching stock
        $('#search-form').submit(function(event){
            event.preventDefault();
            var stockName = $('#stock-searchbar').val();
            // get ticker from stock name
            for(var [key, value] of Object.entries(stocks_mapping)){
                if(value == stockName){
                    addStock(stockName, key, true);
                }
            } 
            $('#stock-searchbar').val('');
        });

        getNews();
        getStocks();
        getStockRecs();
    }

    $('#login').click(function(event){
        var username = $('#username-input').val();
        var password = $('#password-input').val();    
        if(username != "" && password != ""){
            handleLogin(username, password);
        }
    });
});

function handleLogin(username, password){
    //login request to backend, on success store username and age and redirect
    fetch('http://127.0.0.1:8000/user/verify/',
    {
        mode: 'cors',
        method: 'POST',
        body: JSON.stringify({"user_id": username, "password": password})
    }).then(response => {
        return response.json();
    }).then(data => {
        //console.log(data.user_data);
        if(data.status == true){
            console.log("login successful");
            localStorage.setItem('age', data.user_data.Age.toString());
            localStorage.setItem('user', data.user_id);
            window.location.href = "index.html";
        }
    });
}

function getNews(){
    console.log('getting news');
    fetch('http://127.0.0.1:8000/news/display/',
    {
        mode: 'cors',
        method: 'POST',
        body: JSON.stringify({user_id: localStorage.getItem('user')})
    }).then(response => {
        return response.json();
    }).then(data => {
        appendNews(JSON.parse(data.news));
    });
}

function getStocks(){
    //get user's stocks and watchlist
    console.log('getting stocks');
    fetch('http://127.0.0.1:8000/stocks/userstocks/',
    {
        mode: 'cors',
        method: 'POST',
        body: JSON.stringify({user_id: localStorage.getItem('user')})
    }).then(response => {
        return response.json();
    }).then(data => {
        console.log(data);
        data.user_stocks.forEach(stock => {
            appendStock(stocks_mapping[stock.Stock], stock['Current Price'], stock['Current Value']);
        });

        data.user_watchlist.forEach(stock => {
            userWatchist.push(stock.Stock);
            appendWatchlist(stocks_mapping[stock.Stock], stock['Current Price']);
        })
    });   
}

function getStockRecs(){
    //get user's stock reccomendations
    console.log('getting recommendations');
    fetch('http://127.0.0.1:8000/stocks/recommend/',
    {
        mode: 'cors',
        method: 'POST',
        body: JSON.stringify({user_id: localStorage.getItem('user')})
    }).then(response => {
        return response.json();
    }).then(data => {
        console.log(data.recommendations.data);
        data.recommendations.data.forEach(rec => {
            var ticker = rec[0];
            var sector = rec[1];
            var risk = rec[2];
            var price = rec[3];
            var profit = rec[4];
            var name = stocks_mapping[ticker];
            var disableButton = userWatchist.includes(ticker);
            appendStockRec(name, ticker, sector, risk, price, profit, disableButton);
        });
    });   
}

function addStock(stock, ticker, fromSearchBar){
    // api call 
    console.log("adding stock: " + stock);
    console.log(fromSearchBar);
    fetch('http://127.0.0.1:8000/stocks/addstock/',
    {
        mode: 'cors',
        method: 'POST',
        body: JSON.stringify({user_id: localStorage.getItem('user'), stock: ticker})
    }).then(response => {
        return response.json();
    }).then(data => {
        console.log(data);
        if(data.status == true){
            appendWatchlist(stock);
            if(!fromSearchBar){
                //remove from list
                var recNode = document.getElementById("rec-" + ticker);
                if(recNode){
                    recNode.remove();
                }
            }
        }
    });   
}

function appendNews(news){
    console.log(news);
    news.forEach(article => {
        var link = article.url;
        var article_name = article.title;
    
        var linkHtml = '<a target="_blank" href="' + link + '" class="text-dark">'; 
        var news = '<div class="row mb-4 border-bottom pb-2"><div class="col-9"><p class="mb-2"> <strong class="new-news">' + article_name + '</strong></p>';
    
        var item = linkHtml + news;
    
        $('#news').append(item);
    });
    adjustNewsStyle();
}

function appendStock(stock, price, value){
    if(stock != undefined && stock != '' && stock_names.includes(stock)){
        var item = '<div class="text-dark"><div class="row mb-4 border-bottom pb-2"><div class="col-9"><p class="mb-2"><strong class="new-stock">' + stock + '</strong><br><p><b>Current Price:</b> ' + price + '<br><b>Current Value:</b> ' + value + '</p></p></div></div></div>';
        $('#stocks').append(item);
    }
    adjustStockStyle();
}

function appendWatchlist(stock, price, value){
    if(stock != undefined && stock != '' && stock_names.includes(stock)){
        var item = '<div class="text-dark"><div class="row mb-4 border-bottom pb-2"><div class="col-9"><p class="mb-2"><strong class="new-stock">' + stock + '</strong><br><p><b>Current Price:</b> ' + price + '</p></p></div></div></div>';
        $('#watchlist').append(item);
    }
    adjustStockStyle();
}

function appendStockRec(stock, ticker, sector, risk, price, profit, disableButton){
    var nameParam = "'" + stock + "'";
    var tickerParam = "'" + ticker + "'";
    if(risk == "low_risk"){
        risk = "low risk";
    }
    
    var item = '<div id="rec-' + ticker + '" class="text-dark"><div class="row mb-4 border-bottom pb-2"><div class="col-9"><p class="mb-2"><strong>' + stock + '</strong><br><p><b>Sector:</b> ' + sector + '<br><b>Risk:</b> ' + risk + '<br><b>Current Price:</b> ' + price + '<br><b>Profit Margins:</b> ' + profit + '</p>';

    if(!disableButton){
        item += '<button onclick="addStock(' + nameParam + ',' + tickerParam + ', false)" type="button" class="add-btn cursor-pointer">Add to Watchlist</button></div></div></div>'
    }
    else{
        item += '</div></div></div>';
    }

    $('#stock-recs').append(item);
    adjustRecStyle();
}