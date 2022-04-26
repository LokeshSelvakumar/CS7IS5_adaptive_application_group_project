function adjustColor(){
    if(userAge <= 30){
        //blue
        $('#body').addClass('bg-info');
        $('#news-title').addClass('text-info');
        $('#stocks-title').addClass('text-info');
        $('#rec-title').addClass('text-info');
    }
    else if(userAge > 30 && userAge <= 50){
        //green
        $('#body').addClass('bg-success');
        $('#news-title').addClass('text-success');
        $('#stocks-title').addClass('text-success');
        $('#rec-title').addClass('text-success');
    }
    else if(userAge > 50){
        //red
        $('#body').addClass('bg-danger');
        $('#news-title').addClass('text-danger');
        $('#stocks-title').addClass('text-danger');
        $('#rec-title').addClass('text-danger');
    }
}

function adjustFontSize(){
    if(userAge <= 30){
        //blue
        $('#news-title').css('font-size', '16px');
        $('#stocks-title').css('font-size', '16px');
        $('#rec-title').css('font-size', '16px');
    }
    else if(userAge > 30 && userAge <= 50){
        //green
        $('#news-title').css('font-size', '20px');
        $('#stocks-title').css('font-size', '20px');
        $('#rec-title').css('font-size', '20px');
    }
    else if(userAge > 50 && userAge <= 70){
        //red
        $('#news-title').css('font-size', '25px');
        $('#stocks-title').css('font-size', '25px');
        $('#rec-title').css('font-size', '25px');
    }
}

function adjustRecStyle(){
    if(userAge <= 30){
        //blue
        $('.add-btn').addClass('btn btn-primary');
        $('.add-btn').css('font-size', '16px');
        $('.new-rec').css('font-size', '16px');
    }
    else if(userAge > 30 && userAge <= 50){
        //green
        $('.add-btn').addClass('btn btn-warning');
        $('.add-btn').css('font-size', '18px');
        $('.new-rec').css('font-size', '18px');
    }
    else if(userAge > 50 && userAge <= 70){
        //red
        $('.add-btn').addClass('btn btn-dark');
        $('.add-btn').css('font-size', '19px');
        $('.new-rec').css('font-size', '19px');
    }
}

function adjustStockStyle(){
    if(userAge <= 30){
        //blue
        $('.new-stock').css('font-size', '16px');
    }
    else if(userAge > 30 && userAge <= 50){
        //green
        $('.new-stock').css('font-size', '18px');
    }
    else if(userAge > 50 && userAge <= 70){
        //red
        $('.new-stock').css('font-size', '19px');
    }
}

function adjustNewsStyle(){
    if(userAge <= 30){
        //blue
        $('.new-news').css('font-size', '16px');
    }
    else if(userAge > 30 && userAge <= 50){
        //green
        $('.new-news').css('font-size', '18px');
    }
    else if(userAge > 50 && userAge <= 70){
        //red
        $('.new-news').css('font-size', '19px');
    }
}