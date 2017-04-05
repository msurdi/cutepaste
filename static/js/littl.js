(function ($) {

    function ajax($el, url, method, data) {
        $el.trigger("littl-request:start", [$el]);
        $.ajax({
            url: url,
            type: method,
            data: data,
            dataType: 'json',
            headers: {"X-Fewer": true}
        }).done((data, textStatus, jqXHR) => {
            if (!data) {
                data = {};
            }
            $el.trigger("littl-request:success", [$el, data, textStatus, jqXHR]);
        }).fail((jqXHR, textStatus, error) => {
            $el.trigger("littl-request:error", [$el, jqXHR, textStatus, error]);
        }).always((data, textStatus, jqXHR) => {
            $el.trigger("littl-request:complete", [$el, data, textStatus, jqXHR]);
        });
    }

    function click(event) {
        let $this = $(this);
        let method = $this.data("method");
        let url = $this.data("url") || $this.attr("href") || window.location.pathname;
        let includeSelector = $this.data("include");

        if (!method) {
            method = "GET";
        }

        let data = $(includeSelector).serializeArray();
        ajax($this, url, method, data);
        event.preventDefault();
    }

    function submit(event) {
        let $this = $(this);
        let url = $this.attr('action');
        let method = $this.attr('method');

        if (window.FormData === undefined) {
            ajax($this, url, method, $this.serialize());
        } else {
            ajax($this, url, method, new FormData($this[0]), true);
        }
        event.preventDefault();
    }

    function action() {
        let $this = $(this);
        let actions = $this.data("action");
        let targetSelector = $this.data("target");
        let $target = $this;

        if (targetSelector) {
            let foundTarget = $(targetSelector).length > 0;
            if (foundTarget) {
                $target = $(foundTarget);
            }
        }
        if (actions) {
            let parsedActions = _parseActions(actions);
            parsedActions.map(
                (action) => {
                    $target[action.fn].apply($target, action.args)
                }
            )
        }
    }

    function _parseActions(configString) {
        let actions = [];
        configString.split(";").map(
            (parts) => {
                let [fn, argsString] = parts.split(":");
                let args = [];
                if (argsString) {
                    args = argsString.split(",");
                }
                actions.push({fn: fn, args: args});
            }
        );
        return actions;
    }

    // Content modification
    function replace(event, $el, data) {
        $($el.data("replace")).replaceWith(data.html);
    }

    function components(event, $el, data) {
        if (data["components"]) {
            $.each(data["components"], (selector, content) => {
                $(selector).replaceWith(content);
            });
        }
    }

    function script(event, $el, data) {
        if (data["script"]) {
            eval(data["script"]);
        }
    }

    function setupListeners() {
        let $this = $(this);
        let eventNames = $this.data("on");

        eventNames.split(",").map(
            (eventName) => {
                let actions = $this.data("on-" + eventName);
                if (actions) {
                    let parsedActions = _parseActions(actions);
                    parsedActions.map((action) => $(document).on(
                        eventName, () => {
                            $this[action.fn].apply($this, action.args)
                        }));
                }
            }
        )
    }

    function registerHandlers(el) {
        let $el = $(el);
        $el.on("littl-request:success", components);
        $el.on("littl-request:success", script);
        $el.on("littl-request:success", "[data-replace]", replace);
        $el.find("[data-on]").each(setupListeners);

    }

    function mutationsHandler(mutations) {
        mutations.forEach(function (mutation) {
            let newNodes = mutation.addedNodes;
            if (newNodes !== null) {
                let $nodes = $(newNodes);
                $nodes.each(function () {
                    registerHandlers(this);
                });
            }
        });
    }


    // Register DOM events
    $(() => {
        $document = $(document);
        $document.on("click", "a[data-action]", action);
        $document.on("click", "button[data-action]", action);
        $document.on("click", "label[data-action]", action);
        $document.on("change", "input[data-action]", action);

        //data-ajax
        $document.on("click", "button[data-ajax]", click);
        $document.on("click", "label[data-ajax]", click);
        $document.on("click", "a[data-ajax]", click);
        $document.on("change", "input[data-ajax]", click);
        $document.on('submit', 'form[data-ajax]', submit);

        registerHandlers(document);

        let observer = new MutationObserver(mutationsHandler);

        observer.observe(document, {
            attributes: false,
            childList: true,
            characterData: true,
            subtree: true,
        });

    });
})(jQuery);