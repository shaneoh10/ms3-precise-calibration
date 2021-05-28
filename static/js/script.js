  $(document).ready(function () {
      $('.sidenav').sidenav();
      $('.collapsible').collapsible();
      $('.datepicker').datepicker({
          format: "dd mmmm yyyy",
          yearRange: 2,
          showClearBtn: true,
          i18n: {
              done: "Select"
          }
      });
  });
