/*!
  *
  * Copyright
  * Licensed under MIT
  */
// A $( document ).ready() block.
$(document).ready(function () {
    console.log("ready!");


    var header_template = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3809.100 Safari/517.36",
        "Cookies": [
            {
                "name": "user.expires_at",
                "value": "xxxxxx",
                "domain": "www.example.com"
            }],
        "Referer": null,
        "Proxy": null
    };
    $('[name="headers"]').html(JSON.stringify(header_template, null, 4));


    var url_template = "https://invanalabs.ai";
    $('[name="url"]').val(url_template);


    function simulate_loading() {
        $("#response-viewer").html("<p class='text-muted'>loading ...</p>");
        $("#response-img").attr("src", "");

    }

    $("#submit-button").click(function () {


        simulate_loading();

        var url = $("#form [name='url']").val();
        var headers = $("#form [name='headers']").val();
        var timeout = $("#form [name='timeout']").val();
        var viewport = $("#form [name='viewport']").val();
        var take_screenshot = $("#form [name='take_screenshot']").is(":checked");
        if (take_screenshot === true) {
            take_screenshot = 1
        } else {
            take_screenshot = 0;
        }


        let params = (new URL(document.location)).searchParams;
        let token = params.get("token");
        console.log("url", url);
        console.log("headers", headers, JSON.parse(headers));
        var body = {
            "headers": JSON.parse(headers)
        };


        $.ajax({
            type: 'POST',
            url: "/execute?url=" + url + "&timeout=" + timeout + "&viewport=" + viewport
                + "&token=" + token + "&take_screenshot=" + take_screenshot,
            data: JSON.stringify(body),
            contentType: "application/json",
            dataType: 'json'
        })
            .done(function (data) {
                console.log(data);

                data['response']['html'] = "< =truncated= >";
                var screenshot = data['response']['screenshot'];
                console.log("screeenshot", screenshot);
                $("#response-viewer").html(JSON.stringify(data, null, 4));
                $("#response-img").attr("src", "data:image/png;base64," + screenshot);
            })
            .fail(function (error) {
                console.error(error);
            })
            .always(function () {
                // called after done or fail
            });
    })
});