// A $( document ).ready() block.
$(document).ready(function () {
    console.log("ready!");


    var header_template = "" +
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3809.100 Safari/517.36\n" +
        "Cookies:\n" +
        "- name: user.expires_at\n" +
        "  value: xxxxxx\n" +
        "  domain: www.example.com\n" +
        "Referer: null\n" +
        "Proxy: null\n";

    var form_data = "" +
        "form_identifier:\n" +
        "  selector: \"form.login-form\"\n" +
        "  selector_type: \"css\"\n" +
        "  index_number: 0\n" +
        "submit_identifier:\n" +
        "  selector: \".btn-submit\"\n" +
        "fields:\n" +
        "  - selector: \"userLoginId\"\n" +
        "  - selector_type: \"name\"\n" +
        "    field_value: \"hello@example.com\"\n" +
        "  - selector: \"password\"\n" +
        "  - selector_type: \"name\"\n" +
        "    field_value: \"password\"\n";

    // var task_code = "" +
    //     "def simulate(driver=None):\n" +
    //     "    import random\n" +
    //     "    driver.switch_to.default_content()\n" +
    //     "    driver.implicitly_wait(random.randint(0, 2))\n" +
    //     "    print ('Successfully waited for sometime')";
    //
    //
    // var extractors_template = "" +
    //     "- extractor_type: MetaTagExtractor\n" +
    //     "  extractor_id: meta_tags\n" +
    //     "- extractor_type: CustomContentExtractor\n" +
    //     "  extractor_id: content\n" +
    //     "  data_selectors:\n" +
    //     "  - selector_id: title\n" +
    //     "    selector: title\n" +
    //     "    selector_type: css\n" +
    //     "    selector_attribute: text\n" +
    //     "    data_type: RawField";
    //
    // var traversals_template = "" +
    //     "- traversal_id: default_traversal\n" +
    //     "  selector: \"a\"\n" +
    //     "  selector_type: css\n" +
    //     "  selector_attribute: href\n" +
    //     "  data_type: ListStringField\n" +
    //     "  max_requests: 500\n" +
    //     "  next_spider_id: default_spider";

    $('[name="headers"]').html(header_template);
    $('[name="form_data"]').html(form_data);
    // $('[name="task_code"]').html(task_code);
    // $('[name="extractors"]').html(extractors_template);
    // $('[name="traversals"]').html(traversals_template);


    var url_template = "http://invana.io";
    $('[name="url"]').val(url_template);


    function simulate_loading() {
        $("#response-viewer").html("<p class='text-muted'>loading ...</p>");
        $("#response-img").attr("src", "");

    }

    $("#submit-button").click(function () {


        simulate_loading();

        var url = $("#form [name='url']").val();
        var headers = $("#form [name='headers']").val();
        var editor_form_data = $("#form [name='form_data']").val();
        var extractors = null;
        var traversals = null;

        var task_code = null;
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
        var body = {
            "headers": headers,
            "extractors": extractors,
            "traversals": traversals,
            "task_code": task_code,
            "form_data": editor_form_data

        };
        console.log("bodybody", body);

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