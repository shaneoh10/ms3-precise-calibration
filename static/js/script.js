//   Materialize initialization code from https://materializecss.com/ 
$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.tabs').tabs();
    $('.modal').modal();
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "dd mmmm yyyy",
        yearRange: 2,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
    //   Validation for materialize dropdown option select - copied from Code Institute Task Manager Project 
    validateMaterializeSelect();

    function validateMaterializeSelect() {
        let classValid = {
            "border-bottom": "1px solid #4caf50",
            "box-shadow": "0 1px 0 0 #4caf50"
        };
        let classInvalid = {
            "border-bottom": "1px solid #f44336",
            "box-shadow": "0 1px 0 0 #f44336"
        };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({
                "display": "block",
                "height": "0",
                "padding": "0",
                "width": "0",
                "position": "absolute"
            });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
});


// Toggle chevron icon on collapsible headers 
$(".collapsible-header").click(function () {
    $(this).find('.chevron-icon').toggleClass("fa-chevron-right");
});

$('#cal-container').click(function () {
    $('#cal-list > li').each(function () {
        if (!$(this).hasClass('active')) {
            $(this).find('.chevron-icon').addClass('fa-chevron-right');
        }
    });
});


// Flashed message modal pop up https://stackoverflow.com/questions/10233550/launch-bootstrap-modal-on-page-load
$(window).on('load', function () {
    $('#modal1').modal('open');
});


// Change color of pass or fail span - https://api.jquery.com/contains-selector/
$(".pass-or-fail:contains('FAIL')").css("background-color", "#ff5947");
$(".pass-or-fail:contains('PASS')").css("background-color", "#47c46c");


// Toggle between failed, passed or all calibrations on dashboard
$('#failed').click(function () {
    $(".pass-or-fail:contains('PASS')").each(function () {
        $(this).parentsUntil('.chevron-list').css('display', 'none');
    });
    $(".pass-or-fail:contains('FAIL')").each(function () {
        $(this).parentsUntil('.chevron-list').show();
    });
    // https://stackoverflow.com/questions/53063672/expand-all-and-collapse-all-collapsible-accordion-materialize-css/53064634
    var instance = M.Collapsible.getInstance($('.collapsible'));
    const children = instance.$el[0].children.length;
    for (var i = 0; i < children; i++) {
        instance.close(i);
    }
});

$('#passed').click(function () {
    $(".pass-or-fail:contains('FAIL')").each(function () {
        $(this).parentsUntil('.chevron-list').css('display', 'none');
    });
    $(".pass-or-fail:contains('PASS')").each(function () {
        $(this).parentsUntil('.chevron-list').show();
    });
    // https://stackoverflow.com/questions/53063672/expand-all-and-collapse-all-collapsible-accordion-materialize-css/53064634
    var instance = M.Collapsible.getInstance($('.collapsible'));
    const children = instance.$el[0].children.length;
    for (var i = 0; i < children; i++) {
        instance.close(i);
    }
});

$('#all').click(function () {
    $('.pass-or-fail').each(function () {
        $(this).parentsUntil('.chevron-list').show();
    });
    // https://stackoverflow.com/questions/53063672/expand-all-and-collapse-all-collapsible-accordion-materialize-css/53064634
    var instance = M.Collapsible.getInstance($('.collapsible'));
    const children = instance.$el[0].children.length;
    for (var i = 0; i < children; i++) {
        instance.close(i);
    }
});


// Alert user if passwords not matching when registering account
$("#password-check").keyup(function() {
    if($("#reg-password").val() != $("#password-check").val()) {
        $("#password-alert").html("Passwords do not match!");
    } else {
        $("#password-alert").html("");
    } 
});
