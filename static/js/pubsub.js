(function ($) {
    let bus = $({});
    $.fn.subscribe = function () {
        bus.on.apply(bus, arguments);
    };
    $.subscribe = $.fn.subscribe;

    $.fn.unsubscribe = function () {
        bus.off.apply(bus, arguments);
    };
    $.unsubscribe = $.fn.unsubscribe;

    $.fn.publish = function () {
        bus.trigger.apply(bus, arguments);
    };
    $.publish = $.fn.publish;

}(jQuery));