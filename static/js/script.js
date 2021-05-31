//   Materialize initialization code from https://materializecss.com/ 
  $(document).ready(function () {
      $('.sidenav').sidenav();
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
  });

// Toggle chevron icon on collapsible headers 
$(".collapsible-header").click(function() {
    $(this).find('.chevron-icon').toggleClass("fa-chevron-right");
});

$('#cal-container').click(function() {
    $('#cal-list > li').each(function(){
        if (! $(this).hasClass('active')) {
            $(this).find('.chevron-icon').addClass('fa-chevron-right');
        }
    });
});  