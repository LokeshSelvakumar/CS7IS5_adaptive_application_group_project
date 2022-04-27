var stocks_mapping = {};
var stock_names = []
var userAge = -1;
var userWatchlist = [];
//localStorage.setItem('age', '22');

$('document').ready(function(){
    //loading UI
    if(window.location.href == 'http://127.0.0.1:5500/CS7IS5_adaptive_application_group_project/basicUI/index.html'){
        userAge = parseInt(localStorage.getItem('age'));
        
        adjustColor();
        adjustFontSize();
        
        //get ticker -> company name mapping
        $.getJSON('stocks_mapping.json', function(data){
            stocks_mapping = data;
            stock_names = Object.values(stocks_mapping);
            console.log(stock_names.length);
            
            // autocomplete for searchbar
            $('#stock-searchbar').autocomplete({
                source: stock_names
            });
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

            //clear searchbar 
            $('#stock-searchbar').val('');
        });

        getNews();
        getStocks();
        setTimeout(function(){
            getStockRecs();
        }, 1000);
    }

    // login event
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
        if(data.status == true){
            console.log("login successful");
            localStorage.setItem('age', data.user_data.Age.toString());
            localStorage.setItem('user', data.user_id);
            window.location.href = "index.html";
        }
    });
}

function getNews(){
    //request to get user's news
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
            userWatchlist.push(stock.Stock);
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
            var name = stocks_mapping[rec[0]];
            var disableButton = userWatchlist.includes(rec[0]);
            appendStockRec(rec, name, disableButton);
        });
    });   
}

function addStock(stock, ticker){
    // add new stock to user's watchlist
    console.log("adding stock: " + stock);
    fetch('http://127.0.0.1:8000/stocks/addstock/',
    {
        mode: 'cors',
        method: 'POST',
        body: JSON.stringify({user_id: localStorage.getItem('user'), stock: ticker})
    }).then(response => {
        return response.json();
    }).then(data => {
        if(data.status == true){
            window.location.reload();
        }
    });   
}

function appendNews(news){
    //append news to UI
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
    //append new stock to UI
    if(stock != undefined && stock != '' && stock_names.includes(stock)){
        var item = '<div class="text-dark"><div class="row mb-4 border-bottom pb-2"><div class="col-9"><p class="mb-2"><strong class="new-stock">' + stock + '</strong><br><p><b>Current Price:</b> ' + price + '<br><b>Current Value:</b> ' + value + '</p></p></div></div></div>';
        $('#stocks').append(item);
    }
    adjustStockStyle();
}

function appendWatchlist(stock, price){
    //append new stock to watchlist
    if(stock != undefined && stock != '' && stock_names.includes(stock)){
        var item = '<div class="text-dark"><div class="row mb-4 border-bottom pb-2"><div class="col-9"><p class="mb-2"><strong class="new-stock">' + stock + '</strong><br><p><b>Current Price:</b> ' + price + '</p></p></div></div></div>';
        $('#watchlist').append(item);
    }
    adjustStockStyle();
}

function appendStockRec(stock, name, disableButton){
    //append recommendation to watchlist
    var nameParam = "'" + name + "'";
    var tickerParam = "'" + stock[0] + "'";
    if(stock[2] == "low_risk"){
        stock[2] = "low risk";
    }
    
    var item = '<div class="text-dark"><div class="row mb-4 border-bottom pb-2"><div class="col-9"><p class="mb-2"><strong>' + name + '</strong><br><p><b>Sector:</b> ' + stock[1] + '<br><b>Risk:</b> ' + stock[2] + '<br><b>Current Price:</b> ' + stock[3] + '<br><b>Profit Margins:</b> ' + stock[4] + '</p>';

    if(!disableButton){
        item += '<button id="btn-' + stock[0] + '" onclick="addStock(' + nameParam + ',' + tickerParam + ', false)" type="button" class="add-btn cursor-pointer">Add to Watchlist</button></div></div></div>'
    }
    else{
        item += '</div></div></div>';
    }

    $('#stock-recs').append(item);
    adjustRecStyle();
}