// $Id: spoiler.js,v 1.1.2.2 2009/03/11 15:32:40 karthik Exp $

Drupal.behaviors.spoiler = function() {
  $('.spoiler')
    .addClass('spoiler-js')
    .removeClass('spoiler')
    .click(function() {
      $(this).children().toggle('normal');
    })
    .children('.spoiler-warning')
    .html(Drupal.t('<span title="Click to view">Spoiler</span>'))
    .siblings('.spoiler-content')
    .hide();
}
