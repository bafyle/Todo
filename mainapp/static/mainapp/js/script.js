window.onload = function () {
    bootlint.showLintReportForCurrentDocument([], {
        hasProblems: false,
        problemFree: false
    });

    //$('[data-toggle="tooltip"]').tooltip();

    function formatDate(date) {
        return (
            date.getFullYear() + 
            "-"+
            (date.getMonth() + 1) +
            "-" +
            date.getDate()
        );
    }

    var currentDate = formatDate(new Date());

    $(".due-date-button").datepicker({
        format: "dd/mm/yyyy",
        autoclose: true,
        todayHighlight: true,
        startDate: currentDate,
        orientation: "bottom right"
    });

    $(".due-date-button").on("click", function (event) {
        $(".due-date-button")
            .datepicker("show")
            .on("changeDate", function (dateChangeEvent) {
                $(".due-date-button").datepicker("hide");
                $(".clear-due-date-button").removeClass("d-none");
                $(".due-date-label").text(formatDate(dateChangeEvent.date));
                $(".due-date-label").removeClass("d-none");
            });
    });
    
    $(".clear-due-date-button").on("click", function(event) {
        $(".due-date-label").text("Due date not set");
        $(".due-date-label").addClass("d-none");
        $(".clear-due-date-button").addClass("d-none");
    })
};
