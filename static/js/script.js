  $(document).ready(function () {
      $('.sidenav').sidenav();
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
