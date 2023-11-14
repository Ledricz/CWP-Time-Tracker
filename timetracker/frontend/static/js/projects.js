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

function toTitleCase(str) {
    return str.replace(
        /\w\S*/g,
        function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}

function inRange(n, start, end) {
    if (n >= start && n <= end) {
        return n
    }
    return false
}

$(function () {
    const wrap = $("#wrap")
    let add_btn = wrap.find("#add-new-project")
    let save_btn = wrap.find("#save-new-projects")
    let csrf_token = wrap.find("[name='csrfmiddlewaretoken']").val()

    add_btn.on("click", function () {
        $.ajax({
            type: "GET",
            url: "/api/v1/projects/add_new_line/",
            dataType: "html",
        }).always(function (response) {
            save_btn.fadeIn()
            wrap.find("table tbody").append(response)
        })
    })

    save_btn.on("click", function (event) {        
        wrap.find(".error-container").html("&nbsp;")
        save_btn.find(".fa-save").fadeOut()
        save_btn.find(".fa-spinner").fadeIn()

        let input_data = []
        wrap.find(".new-row input[name='name']").each(function (index, item) {
            input_data.push({
                "name": item.value,
                "active": true
            })
        })
        $.ajax({
            type: "POST",
            url: "/api/v1/projects/",
            data: {"data": JSON.stringify(input_data)},
            headers: {
                "X-CSRFToken": csrf_token
            },
            dataType: "application/json",
            traditional: true
        }).always(function (response) {
            save_btn.fadeOut()
            save_btn.find(".fa-spinner").fadeOut()
            save_btn.find(".fa-save").fadeIn()
            
            if (!!response && "status" in response) {
                switch (response.status) {
                    case inRange(response.status, 200, 399):
                        window.location.href = "/projects/"
                    case inRange(response.status, 400, 599):
                        if ("responseText" in response) {
                            let err_msg = convertResponseText($.parseJSON(response.responseText))
                            wrap.find(".error-container").html(err_msg)
                        }
                }
            }
        })
    })

    wrap.on("click", "button.delete-row", function (event) {
        $(this).closest("tr.new-row").remove()
    })

    wrap.find(".curtain").on("click", ".toggle-slide", function (event) {
        let curtain = $(event.delegateTarget)
        let target = this.dataset.target
        curtain.find(target).slideToggle()
    })

})