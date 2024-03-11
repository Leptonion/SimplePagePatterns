function EnterNewParam(url, newKey, newVal){
    var url = new URL(url)
    var search = new URLSearchParams(url.search)
    var currentParam = search.get(newKey)

    if(currentParam){
        splitParam = currentParam.split(",")
        if(jQuery.inArray(newVal, splitParam) >= 0){
            splitParam = $.grep(splitParam, function(val){return val != newVal});
            if(splitParam.length >= 1){
                url.searchParams.set(newKey, splitParam.toString())
            }
            else{
                url.searchParams.delete(newKey, newVal)
            }
        }
        else{
            splitParam.push(newVal)
            url.searchParams.set(newKey, splitParam.toString())
        }
    }
    else{
        url.searchParams.set(newKey, newVal)
    }


    return url.toString()
}

function ChecksActivate(search){
    var url_search = new URLSearchParams(search)

    for(const [key, val] of url_search.entries()){
        vals_array = val.split(',')
        vals_array.forEach(function(item){
            if($('#check-pos-' + key + '-' + item).is(":checked")){

            }
            else{
                $('#check-pos-' + key + '-' + item).prop('checked', true);
            }
        });
    }
}

function EnterSearchKeyword(url){
    var url = new URL(url)
    var text = $('#search-input').val()
    if(text.length >= 1){
        url.searchParams.set('search', text)
    }
    else{
        url.searchParams.delete('search')
    }
    return url
}

function SearchActivate(search){
    var url_search = new URLSearchParams(search)
    var search_word = url_search.get('search')

    if(search_word !== null){
        search_word = search_word.replace('+', ' ')
        $('#search-input').val(search_word)
    }
}

function EnterPage(url, page){
    var url = new URL(url)

    url.searchParams.set('page', page)

    return url
}

function PagesActivate(url, pages){
    var url = new URL(url)
    var current_page = new URLSearchParams(url.search).get('page')

    if(current_page === null){
        current_page = 1
    }

    if(parseInt(current_page) === pages[0]){
        $('#pagination-back').addClass('page-item disabled')
    }
    else{
        $('#pagination-back').addClass('page-item')
    }

    if(parseInt(current_page) === pages[pages.length-1]){
        $('#pagination-up').addClass('page-item disabled')
    }
    else{
        $('#pagination-up').addClass('page-item')
    }

}