function convertResponseText(arr) {
    let res = ""

    Object.keys(arr).forEach(function (key) {
        res += toTitleCase(key).split("_").join(" ")
        res += ": "
        res += arr[key]
        res += "<br>"

    })
    return res
}

function inRange(n, start, end) {
    if (n >= start && n <= end) {
        return n
    }
    return !n
}

function toTitleCase(str) {
    return str.replace(
        /\w\S*/g,
        function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}

$(function () {
    $("#navbar").on("click", ".logout", function (e) {
        $.ajax({
            type: "GET",
            url: "/api/v1/employees/logout/",
            dataType: "application/json",
        }).always(function () {
            window.location.href = "/home/"
        })
    })

    const wrap = $("#wrap");

    wrap.find("form.tt-form").on("click", "[type='submit']", function (event) {
        event.preventDefault();
        let form = $(event.delegateTarget)
        let input_data = serializeForm(form);
        let csrf_token = form.find("[name='csrfmiddlewaretoken']").val()
        form.find(".error-container").html("&nbsp;")
        $.ajax({
            type: form.data().method || "POST",
            url: form.attr("action"),
            data: input_data,
            headers: {
                "X-CSRFToken": csrf_token
            },
            dataType: "application/json",
        }).always(function (response) {
            // TODO: REPLACE .always() with .done() and .fail() after fixing the issue making the Parse Error 
            // Parse error causes .fail() to be always called, even if response is 200 OK 
            if (!!response && "status" in response) {
                // Bypass the Parse Error
                switch (response.status) {
                    case inRange(response.status, 200, 399):
                        window.location.href = form.data().redirect || "/home/"
                    case inRange(response.status, 400, 599):
                        if ("responseText" in response) {
                            let err_msg = convertResponseText($.parseJSON(response.responseText))
                            form.find(".error-container").html(err_msg)
                        }
                }
            }


        })
    })

    function serializeForm($form) {
        let unindexed_array = $form.serializeArray();
        let indexed_array = {};

        $.map(unindexed_array, function (n, i) {
            indexed_array[n['name']] = n['value'];
        });

        return indexed_array;
    }

});
