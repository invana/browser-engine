// A $( document ).ready() block.
$(document).ready(function () {
    console.log("ready!");


    var header_init_template = "" +
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3809.100 Safari/517.36\n" +
        "Cookies:\n" +
        "- name: user.expires_at\n" +
        "  value: xxxxxx\n" +
        "  domain: www.example.com\n" +
        "Referer: null\n" +
        "Proxy: null\n";

    var browser_simulation_template = "" +
        "def simulate(driver=None):\n" +
        "    import random\n" +
        "    driver.switch_to.default_content()\n" +
        "    driver.implicitly_wait(random.randint(0, 2))\n" +
        "    print ('Successfully waited for sometime')";


    var traversals_template = "" +
        "- traversal_id: default_traversal\n" +
        "  selector: \"a\"\n" +
        "  selector_type: css\n" +
        "  selector_attribute: href\n" +
        "  data_type: ListStringField\n" +
        "  max_requests: 500\n" +
        "  next_spider_id: default_spider";

    var json_extraction_template = "- extractor_type: MetaTagExtractor\n" +
        "  extractor_id: meta_tags\n" +
        "- extractor_type: CustomContentExtractor\n" +
        "  extractor_id: content\n" +
        "  data_selectors:\n" +
        "  - selector_id: title\n" +
        "    selector: title\n" +
        "    selector_type: css\n" +
        "    selector_attribute: text\n" +
        "    data_type: RawField\n";


    var url_template = "http://invana.io";
    $('[name="url"]').val(url_template);


    function simulate_loading() {
        $("#response-viewer").html("<p class='text-muted'>loading ...</p>");
        $("#response-img").attr("src", "");

    }

    $("#load-init-headers").click(function () {
        $('[name="init_headers"]').html(header_init_template);

    });


    $(".add-new-task").click(function () {
        var task_length = $(".task-section").length;

        var new_task_type = $("#new-task-type").val();
        console.log("===new_task_type", new_task_type);
        var task_id = "task-" + (parseInt(task_length) + 1);
        var div_template = $("<div class=\"mb-2 task-section\" data-task-id='" + task_id + "' >\n" +
            "    <span class='ml-1'><strong>"+task_id+"</strong></span>\n" +
            "    <a class=\" remove-task\" data-task-id='" + task_id + "' >remove</a>\n" +
            "    <div class=\"clearfix\"></div>\n" +
            // "    <label><strong>Task Type</strong></label>\n" +
            "    <select name=\"task_type\" data-task-id='" + task_id + "' class=\"form-control task_type mb-2 mt-2\">\n" +
            "        <option value=\"browser_simulation\">Browser Simulation</option>\n" +
            "        <option value=\"json_extractor\">JSON Extraction</option>\n" +
            "        <option value=\"get_html\">HTML Extractor</option>\n" +
            "        <option value=\"get_screenshot\">Screenshot</option>\n" +
            "    </select>\n" +
            // "    <label><strong>Task Code</strong></label>\n" +
            "    <textarea name=\"task_code\" data-task-id='" + task_id + "' class=\"form-control task_code \" cols=\"30\" rows=\"10\"></textarea>\n" +
            "<p><a class=\"load-task-template\" data-task-id='" + task_id + "' href=\"javascript:void(0);\">load template</a></p>" +
            "</div>");

        div_template.find(".task_type").val(new_task_type);
        div_template.find('.task_code').show();
        div_template.find('.load-task-template').show();

        if (new_task_type === "get_html" || new_task_type === "get_screenshot") {
            div_template.find('.task_code').hide();
            div_template.find('.load-task-template').hide();
        }
        if (new_task_type === "json_extractor") {
            div_template.find(".task_code").text(json_extraction_template)
        } else if (new_task_type === "browser_simulation") {
            div_template.find(".task_code").text(browser_simulation_template);
        }
        div_template.find(".remove-task").click(function () {
            div_template.remove();
        });

        // assign event listener
        div_template.find(".load-task-template").click(function () {
            var task_id = $(this).attr("data-task-id");
            var task_type = $(".task_type[data-task-id=" + task_id + "]").val();
            var template = "WARNING: TEMPLATE NOT AVAILABLE FOR THIS TASK_TYPE";
            if (task_type === "browser_simulation") {
                template = browser_simulation_template
            } else if (task_type === "json_extractor") {
                template = json_extraction_template
            } else if (task_type === "get_html") {
                template = "# This doesn't need any task_code"
            } else if (task_type === "get_screenshot") {
                template = "# This doesn't need any task_code"
            }
            $('.task_code[data-task-id="' + task_id + '"]').html(template);

        });

        div_template.find('.task_type').change(function (e) {
            console.log("=====e", e);
            div_template.find('.task_code').show();
            if (e.target.value === "get_html" || e.target.value === "get_screenshot") {
                div_template.find('.task_code').hide();
            }
        });


        $("#task-list-content").append(div_template);
    });

    function removeTask() {
        console.log("remove task====");
    }

    $(".header-form").submit(function (e) {


        e.preventDefault();
        simulate_loading();

        var url = $(".header-form [name='url']").val();

        // options here
        var timeout = $("[name='timeout']").val();
        var viewport = $("[name='viewport']").val();

        // payload here
        var init_headers = $("#form [name='init_headers']").val();

        var tasks = {};
        if ($(".task-section").length === 0) {
            alert("Add atleast on task ");
        } else {
            $(".task-section").each(function (task) {
                var task_id = $(this).data("task-id");
                tasks[task_id] = {
                    "task_type": $(this).find('[name= "task_type"]').val(),
                    "task_code": $(this).find('[name= "task_code"]').val(),
                }
            });

            let params = (new URL(document.location)).searchParams;
            let token = params.get("token");
            console.log("url", url);
            var body = {
                "init_headers": init_headers,
                "tasks": tasks
            };
            $.ajax({
                type: 'POST',
                url: "/execute?url=" + url + "&timeout=" + timeout + "&viewport=" + viewport
                    + "&token=" + token,
                data: JSON.stringify(body),
                contentType: "application/json",
                dataType: 'json'
            })
                .done(function (data) {
                    console.log(data);
                    var task_results = data['response']['task_results'];
                    $("#response-container").show();
                    $("#response-viewer").html("");
                    if (task_results) {
                        Object.keys(task_results).forEach(function (key) {
                            var task = task_results[key];
                            console.log("r=====>>>> <<<<======>>> ", task, key);


                            var card_html = $("<div class='card mb-3' id='task-response-" + key + "'>" +
                                "<div class='card-header' >Task Id: <strong>" + key +
                                "</strong> (" + task.task_type + ")" +
                                "</strong> (" + ((task.is_task_success === true) ? "success" : "failed") + ")" +
                                "</strong> ( took " + task.task_elapsed_time_ms + ")" +
                                "</div>" +
                                "<div class='card-body' ></div>" +
                                "</div>");

                            if (task.task_type === "get_screenshot") {
                                var image = $("<img class='img-fluid' />").attr("src", "data:image/png;base64," + task['data']);
                                console.log("======image", image)
                                card_html.find(".card-body").html(image);
                            } else if (task.task_type === "get_html") {
                                card_html.find(".card-body").text(task['data']);

                            }

                            $("#response-viewer").append(card_html);

                        });
                    }

                    $("#response-raw-viewer").text(JSON.stringify(data, null, 4));

                    // data['response']['html'] = "< =truncated= >";
                    var screenshot = data['response']['screenshot'];
                    // $("#response-viewer").html(JSON.stringify(data, null, 4));


                    $("#request-viewer").text(JSON.stringify(data['request'], null, 4));
                    $("#browser-settings-viewer").text(JSON.stringify(data['request']['browser_settings'], null, 4));
                })
                .fail(function (error) {
                    console.error(error);
                })
                .always(function () {
                    // called after done or fail
                });
        }
    })
});