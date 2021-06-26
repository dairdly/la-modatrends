const params = new URLSearchParams(window.location.search);
if (params.has('category')) {
    document.getElementById(params.get('category')).classList.add('list-group-item-danger');
} else if (params.has('type')) {
    document.getElementById(params.get('type')).classList.add('list-group-item-danger');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var setActive = function (elem) {
    document.querySelectorAll(".categories__accordion .list-group-item").forEach(function (item) {
        if (item.classList.contains('list-group-item-danger')) {
            item.classList.remove('list-group-item-danger');
        }
    });
    elem.classList.add('list-group-item-danger');
}

var quantity = function (div) {
    var input = div.childNodes[3];
    div.childNodes[1].onclick = function () {
        if (input.value > 0) {
            input.value = parseInt(input.value) - 1;
        }
    };
    div.childNodes[5].onclick = function () {
        input.value = parseInt(input.value) + 1;
    };
};
document.querySelectorAll('.pr-qty').forEach(function (div) {
    quantity(div);
});

var setProductTotal = function (td) {
    var price = td.childNodes[3].childNodes[2].innerHTML,
        qty = td.childNodes[5].childNodes[1].childNodes[3].value;
    td.childNodes[7].childNodes[2].innerHTML = parseInt(price * qty).toFixed(2);
    let getTotal = function () {
        let value = 0;
        document.querySelectorAll('.total').forEach(
            function (item) {
                value += parseInt(item.innerHTML)
            }
        )
        return value;
    }
    document.querySelector('.cartTotal').innerHTML = getTotal();
};



var sendAmount = function (pk) {
    var xhttp = new XMLHttpRequest();
    let urlEncodedData = "",
        urlEncodedDataPairs = [],
        name;

    let cartqty = ''
    document.querySelectorAll('.cartRow input').forEach(
        function (qty) {
            cartqty += qty.value
            cartqty += ' '
        }
    )
    let data = {
        'total': document.querySelector('.cartTotal').innerHTML,
        'qty': cartqty,
    };
    for (name in data) {
        urlEncodedDataPairs.push(encodeURIComponent(name) + '=' + encodeURIComponent(data[name]));
    }
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log('post response: ' + this.responseText);
            // window.location.href = `${window.location.origin}/checkout/`
            // setTimeout(function(){
            //     console.log('yes')
            //     window.location.reload(); 
            // }, 3000)
        }
    }
    urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');
    xhttp.open('post', `${window.location.origin}/set-amount/`, true);
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.send(urlEncodedData);
}

window.addEventListener('DOMContentLoaded', function () {
    if (window.location.href === `${window.location.origin}/`) {
        document.querySelector('.modal-button').click()
    }
})


// social
var facebookShare = function (link) {
    FB.ui({
        // app_id: 1706235486214058,
        // redirect_uri: link,
        display: 'popup',
        method: 'share',
        href: link,
    }, function (response){});
}

document.querySelectorAll('.categories__item').forEach(function (tab) {
    tab.onclick = function () {
        window.location.href = this.childNodes[1].childNodes[5].href;
    };
});

document.querySelectorAll('.product__item__text').forEach(function (tab) {
    tab.onclick = function () {
        window.location.href = this.childNodes[1].childNodes[0].href;
    };
});