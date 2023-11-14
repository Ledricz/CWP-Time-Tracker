$(function () {
    const wrap = $("#wrap")

    wrap.find(".entry-container").on("click", "a", function (event) {
        let project_id = event.delegateTarget.dataset.project_id
        wrap.find("#create-entry select[name='project_id']").val(project_id).change()
    })

    wrap.find("table").on("click", "td", function (event) {
        let date = $(event.delegateTarget).find("th").eq($(this).index()).data("date")
        wrap.find("#create-entry input[name='date']").val(date).change()
    })
})