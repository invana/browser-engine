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

    var extractors_template = "extractors:\n" +
        "- extractor_type: MetaTagExtractor\n" +
        "  extractor_id: meta_tags\n" +
        "- extractor_type: CustomContentExtractor\n" +
        "  extractor_id: content\n" +
        "  data_selectors:\n" +
        "  - selector_id: title\n" +
        "    selector: title\n" +
        "    selector_type: css\n" +
        "    selector_attribute: text\n" +
        "    data_type: RawField";

    $('[name="headers"]').html(JSON.stringify(header_template, null, 4));
    $('[name="extractors"]').html(extractors_template);


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
        var extractors = $("#form [name='extractors']").val();
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
            "headers": JSON.parse(headers),
            "extractors": extractors
        };
        console.log("bodybody", body);

        $.ajax({
            type: 'POST',
            url: "/render?url=" + url + "&timeout=" + timeout + "&viewport=" + viewport
                + "&token=" + token + "&take_screenshot=" + take_screenshot,
            data: JSON.stringify(body),
            contentType: "application/json",
            dataType: 'json'
        })
            .done(function (data) {
                console.log(data);
                data['response']['html'] = "< =truncated= >";
                var screenshot = data['response']['screenshot'];
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