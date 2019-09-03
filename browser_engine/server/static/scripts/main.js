// A $( document ).ready() block.
$(document).ready(function () {
    console.log("ready!");


    var header_template = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Cookie": "Pycharm-de81e11c=9fcc92ae-1279-46e1-ad4d-bd3026913c4d; csrftoken=gKCVS8MkdL1izAGibdedXmgp8dwrT5McLNbL4V0tsv9L8O4ANGec2i7LsShjlyW3",
        "Referer": null,

    };
    var url_template = "https://invanalabs.ai";


    $('[name="url"]').val(url_template);
    $('[name="headers"]').html(JSON.stringify(header_template, null, 4));


    $("#submit-button").click(function () {

        var url = $("#form [name='url']").val();
        var headers = $("#form [name='headers']").val();
        var timeout = $("#form [name='timeout']").val();
        var viewport = $("#form [name='viewport']").val();
        var enable_screenshot = $("#form [name='take_screenshot']").is(":checked");


        let params = (new URL(document.location)).searchParams;
        let token = params.get("token");
        console.log("url", url);

        console.log("headers", headers, JSON.parse(headers));
        var body = {
            "headers": JSON.parse(headers)
        };
        $.ajax({
            type: 'POST',
            url: "/render?url=" + url + "&timeout=" + timeout + "&viewport=" + viewport +"&token=" + token,
            data: JSON.stringify(body),
            contentType: "application/json",
            dataType: 'json'
        })
            .done(function (data) {
                console.log(data);

                data['response']['html'] = "<truncated>";
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